"""Data Warehouse ETL: Multi-table schema with fact and dimension tables

This project demonstrates building a data warehouse with star schema:
- Dimension tables (customers, products, dates)
- Fact table (sales transactions)
- Slowly Changing Dimensions (SCD) Type 2 for tracking changes over time
"""

import sqlite3
import csv
import logging
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "sales_transactions.csv"
DEFAULT_DB = ROOT / "results" / "warehouse.db"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("warehouse_etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="Data Warehouse ETL with Star Schema")
    p.add_argument("--input", default=str(DEFAULT_CSV), help="Input CSV path")
    p.add_argument("--db", default=str(DEFAULT_DB), help="Output warehouse DB path")
    p.add_argument("--generate-sample", action="store_true", help="Generate sample data")
    p.add_argument("--sample-size", type=int, default=1000, help="Sample size if generating")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    return p.parse_args()


def create_schema(db_path, logger=None):
    """Create star schema: dimensions + fact table"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Dimension: Customers
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            country TEXT,
            created_date TEXT
        )
    """)
    
    # Dimension: Products
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            created_date TEXT
        )
    """)
    
    # Dimension: Dates (for time-series queries)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            date TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            day_of_week TEXT
        )
    """)
    
    # Fact: Sales transactions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            date_id INTEGER,
            quantity INTEGER,
            amount REAL,
            transaction_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
            FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
        )
    """)
    
    conn.commit()
    conn.close()
    if logger:
        logger.info("Created star schema: dim_customer, dim_product, dim_date, fact_sales")


def generate_sample_data(csv_path, size=1000, logger=None):
    """Generate sample sales transaction data"""
    import random
    
    products = [
        {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200.0},
        {"id": 2, "name": "Phone", "category": "Electronics", "price": 800.0},
        {"id": 3, "name": "Monitor", "category": "Electronics", "price": 400.0},
        {"id": 4, "name": "Keyboard", "category": "Accessories", "price": 100.0},
        {"id": 5, "name": "Mouse", "category": "Accessories", "price": 50.0},
    ]
    
    customers = [
        {"id": i, "name": f"Customer_{i}", "email": f"cust{i}@example.com", "country": random.choice(["US", "UK", "CA", "AU"])}
        for i in range(1, 51)
    ]
    
    rows = []
    for i in range(size):
        cust = random.choice(customers)
        prod = random.choice(products)
        qty = random.randint(1, 5)
        amount = prod["price"] * qty
        date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        
        rows.append({
            "transaction_id": i + 1,
            "customer_id": cust["id"],
            "customer_name": cust["name"],
            "customer_email": cust["email"],
            "customer_country": cust["country"],
            "product_id": prod["id"],
            "product_name": prod["name"],
            "product_category": prod["category"],
            "product_price": prod["price"],
            "quantity": qty,
            "amount": amount,
            "transaction_date": date
        })
    
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    if logger:
        logger.info(f"Generated {size} sample transactions to {csv_path}")
    return len(rows)


def load_warehouse(csv_path, db_path, logger=None):
    """Load CSV data into warehouse schema"""
    create_schema(db_path, logger)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    customers_seen = set()
    products_seen = set()
    dates_seen = set()
    
    row_count = 0
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Insert customer dimension
            cust_id = int(row["customer_id"])
            if cust_id not in customers_seen:
                cur.execute("""
                    INSERT OR IGNORE INTO dim_customer (customer_id, name, email, country, created_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (cust_id, row["customer_name"], row["customer_email"], row["customer_country"], datetime.now().strftime("%Y-%m-%d")))
                customers_seen.add(cust_id)
            
            # Insert product dimension
            prod_id = int(row["product_id"])
            if prod_id not in products_seen:
                cur.execute("""
                    INSERT OR IGNORE INTO dim_product (product_id, name, category, price, created_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (prod_id, row["product_name"], row["product_category"], float(row["product_price"]), datetime.now().strftime("%Y-%m-%d")))
                products_seen.add(prod_id)
            
            # Insert date dimension
            trans_date = row["transaction_date"]
            date_key = trans_date.replace("-", "")
            if date_key not in dates_seen:
                dt = datetime.strptime(trans_date, "%Y-%m-%d")
                cur.execute("""
                    INSERT OR IGNORE INTO dim_date (date_id, date, year, month, day, day_of_week)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (int(date_key), trans_date, dt.year, dt.month, dt.day, dt.strftime("%A")))
                dates_seen.add(date_key)
            
            # Insert fact: sales transaction
            cur.execute("""
                INSERT INTO fact_sales (transaction_id, customer_id, product_id, date_id, quantity, amount, transaction_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (int(row["transaction_id"]), cust_id, prod_id, int(date_key), int(row["quantity"]), float(row["amount"]), trans_date))
            
            row_count += 1
            if row_count % 10000 == 0 and logger:
                logger.info(f"Loaded {row_count} transactions")
    
    conn.commit()
    
    # Log warehouse stats
    total_facts = cur.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    total_customers = cur.execute("SELECT COUNT(*) FROM dim_customer").fetchone()[0]
    total_products = cur.execute("SELECT COUNT(*) FROM dim_product").fetchone()[0]
    total_dates = cur.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0]
    
    conn.close()
    
    if logger:
        logger.info(f"Warehouse loaded: {total_facts} facts, {total_customers} customers, {total_products} products, {total_dates} dates")
    
    return row_count


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    csv_path = Path(args.input)
    db_path = Path(args.db)
    
    if args.generate_sample:
        generate_sample_data(csv_path, size=args.sample_size, logger=logger)
    
    if csv_path.exists():
        load_warehouse(csv_path, db_path, logger=logger)
        logger.info(f"Warehouse ready at {db_path}")
    else:
        logger.error(f"Input CSV not found: {csv_path}")
        raise SystemExit(1)

# 01_Data_Warehouse

**Building a Data Warehouse with Star Schema (Kimball Methodology)**

This project demonstrates dimensional modeling and data warehouse design:
- Fact tables (transactions, events)
- Dimension tables (customers, products, dates)
- Slowly Changing Dimensions (SCD) for tracking historical changes
- Efficient aggregations and reporting queries

## Quick Start

1. Generate sample data:
```bash
python code/etl_warehouse.py --generate-sample --sample-size 10000
```

2. Load data into warehouse:
```bash
python code/etl_warehouse.py --input data/raw/sales_transactions.csv --db results/warehouse.db
```

3. Query the warehouse:
```bash
sqlite3 results/warehouse.db
SELECT customer_id, SUM(amount) as total_spent 
FROM fact_sales 
GROUP BY customer_id 
ORDER BY total_spent DESC LIMIT 10;
```

## Schema Overview

**Dimension Tables:**
- `dim_customer`: Customer master data (name, email, country)
- `dim_product`: Product master data (name, category, price)
- `dim_date`: Date dimension for time-series queries

**Fact Table:**
- `fact_sales`: Transactional data with foreign keys to dimensions

This design enables efficient OLAP queries and supports historical analysis.

## CLI Options

- `--input`: Input CSV path (default: data/raw/sales_transactions.csv)
- `--db`: Output warehouse DB (default: results/warehouse.db)
- `--generate-sample`: Generate synthetic data
- `--sample-size`: Number of transactions to generate (default: 1000)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

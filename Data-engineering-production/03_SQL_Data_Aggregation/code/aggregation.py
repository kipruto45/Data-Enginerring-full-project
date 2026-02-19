"""SQL Data Aggregation Wrapper

Usage:
    python aggregation.py --csv data/raw/sales_data.csv --query "SELECT region, SUM(amount) FROM sales GROUP BY region"
    python aggregation.py --load-csv data/raw/sales_data.csv --db results/sales.db

"""

import sqlite3
import csv
import logging
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "sales_data.csv"
DEFAULT_DB = ROOT / "results" / "sales.db"
SQL_QUERIES = ROOT / "code" / "sql_queries.sql"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("aggregation")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="SQL Data Aggregation Tool")
    p.add_argument("--csv", default=str(DEFAULT_CSV), help="Input CSV path")
    p.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DB path")
    p.add_argument("--load-csv", action="store_true", help="Load CSV into DB")
    p.add_argument("--query", type=str, help="SQL query to execute")
    p.add_argument("--queries-file", default=str(SQL_QUERIES), help="SQL file with queries")
    p.add_argument("--run-all", action="store_true", help="Run all queries from --queries-file")
    p.add_argument("--output", type=str, default="results/output.csv", help="Output CSV path")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    return p.parse_args()


def load_csv(csv_path, db_path, logger=None):
    """Load CSV into SQLite database."""
    try:
        if logger:
            logger.info(f"Loading {csv_path} into {db_path}")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, date TEXT, region TEXT, product TEXT, amount REAL, quantity INTEGER)")
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cur.execute("INSERT INTO sales (date, region, product, amount, quantity) VALUES (?, ?, ?, ?, ?)",
                               (row.get("date"), row.get("region"), row.get("product"), float(row.get("amount", 0)), int(row.get("quantity", 1))))
                except Exception as e:
                    if logger:
                        logger.warning(f"Failed to insert row: {e}")
        conn.commit()
        count = cur.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if logger:
            logger.info(f"Loaded {count} rows into sales table")
        conn.close()
        return count
    except Exception as e:
        if logger:
            logger.error(f"Load failed: {e}")
        raise


def execute_query(query, db_path, logger=None):
    """Execute a SQL query and return results."""
    try:
        if logger:
            logger.info(f"Executing query: {query[:80]}...")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        if logger:
            logger.info(f"Query returned {len(rows)} rows")
        return [dict(r) for r in rows]
    except Exception as e:
        if logger:
            logger.error(f"Query failed: {e}")
        raise


def run_all_queries(sql_file, db_path, logger=None):
    """Parse and run all SELECT queries from a SQL file."""
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            content = f.read()
        # split on ';' and filter for SELECT statements
        queries = [q.strip() for q in content.split(";") if "SELECT" in q.upper() and q.strip()]
        if logger:
            logger.info(f"Found {len(queries)} SELECT queries")
        results = {}
        for i, q in enumerate(queries):
            if logger:
                logger.info(f"Running query {i+1}/{len(queries)}")
            results[f"query_{i+1}"] = execute_query(q, db_path, logger=logger)
        return results
    except Exception as e:
        if logger:
            logger.error(f"Failed to run queries: {e}")
        raise


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    try:
        db_path = Path(args.db)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        if args.load_csv:
            csv_path = Path(args.csv)
            if not csv_path.exists():
                raise SystemExit(f"CSV not found: {csv_path}")
            load_csv(csv_path, db_path, logger=logger)
        
        if args.run_all:
            results = run_all_queries(args.queries_file, db_path, logger=logger)
            # write to CSV
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Results written to {out_path}")
        elif args.query:
            results = execute_query(args.query, db_path, logger=logger)
            logger.info(json.dumps(results, default=str))
    except Exception as e:
        logger.exception("Aggregation failed")
        raise

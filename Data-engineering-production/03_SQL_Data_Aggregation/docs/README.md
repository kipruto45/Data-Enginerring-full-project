# 03_SQL_Data_Aggregation

SQL query examples and Python wrapper for data aggregation on SQLite.

## Quick start

1. Install (if needed): `pip install -r ../requirements.txt` (none required for basic SQLite)
2. Load CSV data into DB:
   ```bash
   python code/aggregation.py --csv data/raw/sales_data.csv --db results/sales.db --load-csv
   ```
3. Run a query:
   ```bash
   python code/aggregation.py --db results/sales.db --query "SELECT region, SUM(amount) FROM sales GROUP BY region"
   ```
4. Run all queries:
   ```bash
   python code/aggregation.py --db results/sales.db --run-all
   ```

## Features

- Python wrapper around SQL queries (CSV → SQLite → queries)
- Pre-defined queries in `code/sql_queries.sql`
- Logging with execution details
- Error handling and retry logic

## CLI Options

- `--csv PATH` : Input CSV path
- `--db PATH` : SQLite DB path (default: `results/sales.db`)
- `--load-csv` : Load CSV into DB first
- `--query SQL` : Execute a single SQL query
- `--run-all` : Run all SELECT queries from `sql_queries.sql`
- `--output PATH` : Output CSV (for batch runs)


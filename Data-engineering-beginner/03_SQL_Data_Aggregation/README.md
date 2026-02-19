# 03_SQL_Data_Aggregation

Python-assisted SQL aggregation workflow: load CSV into SQLite, run ad hoc queries, and execute query batches from SQL files.

## Capabilities

- Generate synthetic sales data
- Load CSV into SQLite table `sales`
- Run one SQL query from CLI
- Run all `SELECT` queries from a SQL file
- Log query execution and row counts

## Project Structure

```text
03_SQL_Data_Aggregation/
├── code/
│   ├── aggregation.py
│   ├── generate_sales_data.py
│   └── sql_queries.sql
├── data/raw/
├── results/
├── tests/test_aggregation.py
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
python code/generate_sales_data.py --rows 100000 --out data/raw/sales_data_large.csv
python code/aggregation.py --csv data/raw/sales_data_large.csv --db results/sales.db --load-csv
python code/aggregation.py --db results/sales.db --query "SELECT region, SUM(amount) AS total FROM sales GROUP BY region ORDER BY total DESC"
```

Run all queries from SQL file:

```bash
python code/aggregation.py --db results/sales.db --queries-file code/sql_queries.sql --run-all
```

## CLI Options (`code/aggregation.py`)

- `--csv`: Input CSV path
- `--db`: SQLite database path
- `--load-csv`: Load CSV into `sales`
- `--query`: Execute one SQL query
- `--queries-file`: SQL file path for batch runs
- `--run-all`: Execute all `SELECT` statements in the SQL file
- `--output`: Output path placeholder for batch mode
- `--log-level`: Logging level

## Testing

```bash
pytest -q tests
```

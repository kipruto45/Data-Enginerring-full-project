# 01_Data_Warehouse

Build a star-schema warehouse from transactional CSV input using SQLite.

## What You Learn

- Fact and dimension modeling (`fact_sales`, `dim_customer`, `dim_product`, `dim_date`)
- CSV-to-warehouse ETL patterns
- Basic dimensional query workflows

## Quick Start

```bash
pip install -r requirements.txt
python code/etl_warehouse.py --generate-sample --sample-size 10000
python code/etl_warehouse.py --input data/raw/sales_transactions.csv --db results/warehouse.db
```

## Verify

```bash
sqlite3 results/warehouse.db "SELECT COUNT(*) FROM fact_sales;"
```

See detailed runbook in `docs/README.md`.

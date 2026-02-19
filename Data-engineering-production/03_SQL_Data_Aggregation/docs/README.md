# 03_SQL_Data_Aggregation

Runbook for loading sales data and executing SQL aggregations.

## Load Data

```bash
python code/aggregation.py --csv data/raw/sales_data.csv --db results/sales.db --load-csv
```

## Execute a Query

```bash
python code/aggregation.py \
  --db results/sales.db \
  --query "SELECT product, SUM(amount) AS revenue FROM sales GROUP BY product ORDER BY revenue DESC"
```

## Execute Query Batch

```bash
python code/aggregation.py --db results/sales.db --queries-file code/sql_queries.sql --run-all
```

## Generate Large Test Data

```bash
python code/generate_sales_data.py --rows 100000 --out data/raw/sales_data_large.csv
```

## Validation

```bash
pytest -q tests
```

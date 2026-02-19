# 03_SQL_Data_Aggregation

This starter project provides SQL scaffolding for sales aggregation.

## Files

- `code/sql_queries.sql`: Base table DDL and sample query
- `data/raw/sales_data.csv`: Input data sample

## Suggested Workflow

1. Create a SQLite database.
2. Run `code/sql_queries.sql`.
3. Load `data/raw/sales_data.csv` into `sales`.
4. Execute aggregation queries for reporting.

Example aggregation:

```sql
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY total DESC;
```

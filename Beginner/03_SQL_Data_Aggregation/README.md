# 03_SQL_Data_Aggregation

Starter SQL aggregation project using a sample sales CSV and query template file.

## What Is Included

- `data/raw/sales_data.csv`: Starter sales dataset
- `code/sql_queries.sql`: SQL table definition and sample aggregation query
- `docs/README.md`: Practical usage notes

## Quick Start (SQLite CLI)

```bash
cd Beginner/03_SQL_Data_Aggregation
sqlite3 results/sales.db < code/sql_queries.sql
```

Then import your CSV (using your local SQLite import workflow) and run aggregation queries such as:

```sql
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY total DESC;
```

## Notes

- This folder is intentionally lightweight and SQL-first.
- For a full Python-driven implementation with tests, use `Data-engineering-beginner/03_SQL_Data_Aggregation`.

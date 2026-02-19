# Beginner Data Engineering Projects

This track introduces core data engineering patterns with small, practical projects you can run locally.

## Projects

1. `01_Simple_ETL_CSV_to_DB` - CSV to SQLite ETL with batching, retries, and benchmarking.
2. `02_CSV_Excel_Cleaning` - Data cleaning workflows for CSV/XLSX using pandas.
3. `03_SQL_Data_Aggregation` - Starter SQL aggregation project with sample sales data and query templates.
4. `04_Weather_Data_API` - Starter weather ETL script with placeholder API integration.
5. `05_Movie_Dataset_ETL` - Starter movie dataset ETL with genre aggregation.

## Quick Start

```bash
cd Beginner/01_Simple_ETL_CSV_to_DB
pip install -r requirements.txt
python code/generate_sample_data.py --rows 10000
python code/etl_pipeline.py --input data/raw/sample_data_large.csv --db results/output.db --batch-size 1000 --fast
```

## Notes

- Projects `03`, `04`, and `05` in this folder are intentionally lightweight starter versions.
- For expanded implementations with broader test coverage, use `Data-engineering-beginner/`.

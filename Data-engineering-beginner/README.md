# Data Engineering Beginner Track

A complete beginner-to-practice track with five end-to-end projects covering ETL, cleaning, SQL aggregation, and API-style pipelines.

## Projects

1. `01_Simple_ETL_CSV_to_DB` - Streaming CSV to SQLite with batching, retries, benchmark tooling, and tests.
2. `02_CSV_Excel_Cleaning` - Configurable cleaning pipeline with pandas, profiling, and unit tests.
3. `03_SQL_Data_Aggregation` - CSV to SQLite loading plus reusable SQL query execution helpers.
4. `04_Weather_Data_API` - Weather-style dataset ETL with generator, pipeline, smoke tests, and validation tests.
5. `05_Movie_Dataset_ETL` - Movie dataset ETL with scalable loading patterns and test coverage.

## Common Structure

Each project includes:

- `code/` for runnable scripts
- `data/raw/` for input datasets
- `results/` for generated outputs
- `tests/` for pytest suites
- `docs/README.md` for project-specific details

## Getting Started

```bash
cd Data-engineering-beginner/01_Simple_ETL_CSV_to_DB
pip install -r requirements.txt
python code/etl_pipeline.py --help
pytest -q
```

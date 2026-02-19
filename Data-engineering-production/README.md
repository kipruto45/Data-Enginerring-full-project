# Data Engineering Production Track

Production-focused versions of the core beginner projects with emphasis on reliability, repeatable execution, and operational readiness.

## Projects

1. `01_Simple_ETL_CSV_to_DB`
2. `02_CSV_Excel_Cleaning`
3. `03_SQL_Data_Aggregation`
4. `04_Weather_Data_API`
5. `05_Movie_Dataset_ETL`

## What This Track Emphasizes

- Stable CLI interfaces for repeatable jobs
- Logging and retry-oriented execution paths
- Benchmark-friendly workloads
- Testable project structure with `pytest`

## Quick Start

```bash
cd Data-engineering-production/01_Simple_ETL_CSV_to_DB
pip install -r requirements.txt
python code/etl_pipeline.py --help
pytest -q
```

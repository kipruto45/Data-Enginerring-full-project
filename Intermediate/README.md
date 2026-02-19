# Intermediate Data Engineering Projects

Advanced projects that build on ETL fundamentals with orchestration, warehouse modeling, API resiliency, time-series processing, and text pipelines.

## Projects

1. `01_Data_Warehouse` - Star-schema warehouse ETL with fact and dimension loading.
2. `02_Airflow_ETL_Pipeline` - Airflow DAG orchestration with task dependencies and retries.
3. `03_API_Data_Integration` - Paginated API ingestion with retries, normalization, and CSV export.
4. `04_IoT_Sensor_Data_Collection` - IoT ingestion with anomaly detection and hourly aggregates.
5. `05_Twitter_Reddit_Data_Pipeline` - Social data preprocessing and analytics-ready feature extraction.

## Quick Start

```bash
cd Intermediate/01_Data_Warehouse
pip install -r requirements.txt
python code/etl_warehouse.py --help
```

## Suggested Learning Order

1. Start with `01_Data_Warehouse`.
2. Move to `02_Airflow_ETL_Pipeline` for orchestration concepts.
3. Continue with `03`, `04`, and `05` for API, time-series, and text-processing patterns.

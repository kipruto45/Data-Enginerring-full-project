# Data Engineering Projects Portfolio

A structured, hands-on repository of data engineering projects built with Python.  
It is designed as a progression from foundational ETL workflows to advanced orchestration and analytics pipelines.

## Highlights

- 3 learning tracks with increasing complexity
- 15 core projects covering ETL, APIs, SQL, warehousing, Airflow, and time-series data
- CLI-driven scripts for reproducible local runs
- Test suites with `pytest`
- CI workflow in `.github/workflows/ci.yml`
- Project-level docs in each `docs/README.md`

## Tracks

| Track | Directory | Focus | Projects |
| --- | --- | --- | --- |
| Beginner | `Beginner/` | ETL foundations, cleaning, SQL aggregation, API ingestion | 5 |
| Intermediate | `Intermediate/` | Warehousing, orchestration, resilient API integrations, IoT, social pipelines | 5 |
| Production | `Data-engineering-production/` | Production-ready mirrors of beginner projects | 5 |

Note: `Data-engineering-beginner/` is an alternate beginner copy retained in the repo.

## Project Catalog

### Beginner (`Beginner/`)

1. `01_Simple_ETL_CSV_to_DB` - CSV to SQLite ETL, batching, retries, benchmarking
2. `02_CSV_Excel_Cleaning` - Data cleaning and validation workflows
3. `03_SQL_Data_Aggregation` - SQL-based aggregation and reporting patterns
4. `04_Weather_Data_API` - API-style weather dataset ingestion and transformation
5. `05_Movie_Dataset_ETL` - Movie dataset extraction and transformation pipeline

### Intermediate (`Intermediate/`)

1. `01_Data_Warehouse` - Star-schema warehouse ETL with dimensional modeling
2. `02_Airflow_ETL_Pipeline` - DAG-based workflow orchestration with Apache Airflow
3. `03_API_Data_Integration` - Paginated API ingestion with retries and normalization
4. `04_IoT_Sensor_Data_Collection` - Time-series ingestion, anomaly handling, aggregation
5. `05_Twitter_Reddit_Data_Pipeline` - Social text processing and analytics-ready outputs

### Production (`Data-engineering-production/`)

1. `01_Simple_ETL_CSV_to_DB`
2. `02_CSV_Excel_Cleaning`
3. `03_SQL_Data_Aggregation`
4. `04_Weather_Data_API`
5. `05_Movie_Dataset_ETL`

## Repository Structure

```text
DATA/
├── Beginner/
├── Intermediate/
├── Data-engineering-production/
├── Data-engineering-beginner/
├── .github/workflows/ci.yml
└── COMPLETION_SUMMARY.md
```

Each project typically includes:

- `code/` - main scripts
- `data/raw/` - input datasets
- `results/` - generated outputs (CSV/DB/artifacts)
- `tests/` - unit/integration tests
- `docs/README.md` - project-specific documentation
- `requirements.txt` - dependencies

## Quick Start

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 2. Install dependencies for a target project

```bash
pip install -r Beginner/01_Simple_ETL_CSV_to_DB/requirements.txt
```

### 3. Run a sample beginner pipeline

```bash
python Beginner/01_Simple_ETL_CSV_to_DB/code/generate_sample_data.py \
  --rows 10000 \
  --out Beginner/01_Simple_ETL_CSV_to_DB/data/raw/sample_data_demo.csv

python Beginner/01_Simple_ETL_CSV_to_DB/code/etl_pipeline.py \
  --input Beginner/01_Simple_ETL_CSV_to_DB/data/raw/sample_data_demo.csv \
  --db Beginner/01_Simple_ETL_CSV_to_DB/results/demo_output.db \
  --batch-size 1000 \
  --fast
```

### 4. Run an intermediate API pipeline

```bash
pip install -r Intermediate/03_API_Data_Integration/requirements.txt
python Intermediate/03_API_Data_Integration/code/api_etl.py \
  --api https://jsonplaceholder.typicode.com/posts \
  --output Intermediate/03_API_Data_Integration/results/api_data.csv \
  --batch-size 10
```

## Docker

Run the repository in a consistent containerized environment.

### 1. Build image

```bash
docker compose build
```

### 2. Open an interactive shell in container

```bash
docker compose run --rm workspace
```

### 3. Run tests in container

```bash
docker compose run --rm workspace pytest -q
```

### 4. Run a project command in container

```bash
docker compose run --rm workspace \
  python Beginner/01_Simple_ETL_CSV_to_DB/code/etl_pipeline.py \
  --input Beginner/01_Simple_ETL_CSV_to_DB/data/raw/sample_data.csv \
  --db Beginner/01_Simple_ETL_CSV_to_DB/results/output.db
```

### Airflow note in Docker

This Docker image is focused on project scripts and tests.  
For Airflow, you can still validate DAG logic using:

```bash
docker compose run --rm workspace \
  python Intermediate/02_Airflow_ETL_Pipeline/code/dry_run.py --verbose
```

## Testing

Run all tests:

```bash
pytest -q
```

Run tests for one project:

```bash
pytest Beginner/01_Simple_ETL_CSV_to_DB/tests -q
```

## Airflow Project Note

`Intermediate/02_Airflow_ETL_Pipeline` requires an Apache Airflow runtime.  
See `Intermediate/02_Airflow_ETL_Pipeline/docs/README.md` for setup and DAG execution steps.

## Documentation

For deep dives, open:

- `Beginner/README.md`
- `Intermediate/README.md`
- `Data-engineering-production/README.md`
- Individual project docs under each `docs/README.md`

## Contributing

1. Create a branch.
2. Make focused changes in a specific project folder.
3. Run `pytest -q` locally.
4. Open a pull request with a clear summary and test evidence.

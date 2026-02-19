# 04_Weather_Data_API

Runbook for weather ETL pipeline execution.

## Generate Input Data

```bash
python code/generate_weather_data.py --rows 50000 --out data/raw/weather_observations_large.csv
```

## Run ETL

```bash
python code/weather_etl_pipeline.py \
  --input data/raw/weather_observations_large.csv \
  --db results/weather_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

## Validate

```bash
pytest -q tests
```

## Output Tables

- `weather` (in SQLite DB): loaded weather observations

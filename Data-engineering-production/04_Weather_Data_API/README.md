# 04_Weather_Data_API

Streaming weather-data ETL from CSV to SQLite with optional performance optimizations and retry handling.

## Capabilities

- Generate synthetic weather observations
- Stream-transform-load into SQLite in configurable batches
- Optional SQLite PRAGMA optimizations via `--fast`
- Retry loop for transient SQLite operational errors
- Smoke and unit tests

## Project Structure

```text
04_Weather_Data_API/
├── code/
│   ├── weather_etl_pipeline.py
│   ├── generate_weather_data.py
│   └── weather_etl.py
├── data/raw/
├── results/
├── tests/
└── requirements.txt
```

## Quick Start

```bash
python code/generate_weather_data.py --rows 100000 --out data/raw/weather_observations_large.csv

python code/weather_etl_pipeline.py \
  --input data/raw/weather_observations_large.csv \
  --db results/weather_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

Optional summary script:

```bash
python code/weather_etl.py
```

## Testing

```bash
pytest -q tests
```

## CLI Options (`code/weather_etl_pipeline.py`)

- `--input, -i`: Input CSV path
- `--db`: Output SQLite DB path
- `--batch-size`: Rows per transaction
- `--progress`: Progress logging interval
- `--fast`: Enable SQLite WAL/synchronous optimizations
- `--max-retries`: Retry attempts
- `--retry-delay`: Delay between retries
- `--log-level`: Logging level

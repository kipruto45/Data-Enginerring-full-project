# 05_Movie_Dataset_ETL

Streaming movie-data ETL from CSV to SQLite with batching, retry logic, and optional fast-write settings.

## Capabilities

- Generate synthetic movie datasets
- Stream-transform-load into SQLite
- Batch insert tuning and progress logging
- Retry handling for transient DB write failures
- Smoke and unit tests

## Project Structure

```text
05_Movie_Dataset_ETL/
├── code/
│   ├── movie_etl_pipeline.py
│   ├── generate_movies_data.py
│   └── movie_etl.py
├── data/raw/
├── results/
├── tests/
└── requirements.txt
```

## Quick Start

```bash
python code/generate_movies_data.py --rows 100000 --out data/raw/movies_large.csv

python code/movie_etl_pipeline.py \
  --input data/raw/movies_large.csv \
  --db results/movies_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

Optional aggregation script:

```bash
python code/movie_etl.py
```

## Testing

```bash
pytest -q tests
```

## CLI Options (`code/movie_etl_pipeline.py`)

- `--input, -i`: Input CSV path
- `--db`: Output SQLite DB path
- `--batch-size`: Rows per transaction
- `--progress`: Progress logging interval
- `--fast`: Enable SQLite WAL/synchronous optimizations
- `--max-retries`: Retry attempts
- `--retry-delay`: Delay between retries
- `--log-level`: Logging level

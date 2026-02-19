# 01_Simple_ETL_CSV_to_DB

A lightweight ETL pipeline that reads CSV records, applies a small transformation, and loads them into SQLite.

## Capabilities

- Streaming read to avoid loading entire files into memory
- Batched inserts for better write performance
- Optional SQLite speed optimizations via `--fast`
- Retry handling for transient database errors
- Benchmark and smoke-test scripts

## Project Structure

```text
01_Simple_ETL_CSV_to_DB/
├── code/
│   ├── etl_pipeline.py
│   ├── generate_sample_data.py
│   ├── benchmark_etl.py
│   └── smoke_test_etl.py
├── data/raw/
├── results/
├── tests/
└── requirements.txt
```

## Quick Start

```bash
pip install -r requirements.txt

python code/generate_sample_data.py \
  --rows 100000 \
  --out data/raw/sample_data_large.csv

python code/etl_pipeline.py \
  --input data/raw/sample_data_large.csv \
  --db results/output_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

## Benchmarking

```bash
python code/benchmark_etl.py \
  --csv data/raw/sample_data_large.csv \
  --batch-sizes 1000 5000 \
  --repeats 1 \
  --fast
```

## Testing

```bash
pytest -q tests
python code/smoke_test_etl.py
```

## CLI Options (`code/etl_pipeline.py`)

- `--input, -i`: Input CSV path
- `--db`: Output SQLite database path
- `--batch-size`: Rows per insert transaction
- `--progress`: Progress logging interval (rows)
- `--create-index`: Create index on `name` after load
- `--fast`: Enable SQLite PRAGMA speed optimizations
- `--max-retries`: Retry attempts on transient DB errors
- `--retry-delay`: Base retry delay in seconds
- `--log-level`: Logging verbosity

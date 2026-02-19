# 01_Simple_ETL_CSV_to_DB

Reference guide for running the CSV-to-SQLite ETL pipeline.

## Run Pipeline

```bash
python code/etl_pipeline.py \
  --input data/raw/sample_data.csv \
  --db results/output.db
```

## Useful Variants

```bash
python code/etl_pipeline.py \
  --input data/raw/sample_data_large.csv \
  --db results/output_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

```bash
python code/etl_pipeline.py --create-index
```

## Supporting Scripts

- `code/generate_sample_data.py`: Generate synthetic CSV data
- `code/benchmark_etl.py`: Benchmark ETL throughput by batch size
- `code/smoke_test_etl.py`: Validate that loaded row counts match source data

## Testing

```bash
pytest -q tests
```

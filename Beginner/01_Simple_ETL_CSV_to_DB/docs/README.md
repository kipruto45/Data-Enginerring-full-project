# 01_Simple_ETL_CSV_to_DB

Simple ETL pipeline that reads a CSV and writes into an SQLite database.

How to run:

- Ensure you have Python 3.8+
- Run the basic pipeline: `python code/etl_pipeline.py`
- Run with a different input or DB: `python code/etl_pipeline.py --input data/raw/sample_data_large.csv --db results/output_large.db`

Options (useful for large files):

- `--batch-size N` : number of rows per DB transaction (default 1000)
- `--progress N` : print progress every N rows (0 to disable)
- `--create-index` : create an index on `name` after loading
- `--fast` : enable PRAGMA optimizations (WAL + synchronous=OFF) for faster bulk inserts

What it does:
- Streams rows from CSV (does not load entire file into memory)
- Applies a minimal transform (`name` title-cased)
- Inserts rows in batches into SQLite (faster for large files)

Notes:
- This is a starter example; extend transforms and add logging/tests as needed.
- A smoke test is available at `code/smoke_test_etl.py` to validate row counts for large files.

Testing & CI:

- Unit and integration tests are included under `tests/` (requires `pytest`).
- A GitHub Actions workflow at `.github/workflows/ci.yml` runs the tests on push and PR.
- Install dev deps: `pip install -r requirements.txt` (in the project folder).

Benchmarking & performance tuning:

- Use `code/benchmark_etl.py` to compare throughput for different `--batch-sizes` and generate `results/benchmark_results.csv`.
- For fastest bulk loads, use `--fast` with ETL (enables PRAGMA optimizations), but be aware of durability tradeoffs.


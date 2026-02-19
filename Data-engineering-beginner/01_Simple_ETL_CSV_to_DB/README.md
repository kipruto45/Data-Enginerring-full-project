# 01_Simple_ETL_CSV_to_DB

**Simple ETL: CSV → SQLite (beginner-friendly)** ✅

This project demonstrates a lightweight ETL workflow that reads CSV files, applies small transformations, and writes results into an SQLite database. It is designed to be easy to run locally, testable, and educative for beginners learning data engineering patterns.

---

## Project layout

```
01_Simple_ETL_CSV_to_DB/
├─ code/
│  ├─ etl_pipeline.py            # Main ETL (streaming, batching, CLI options)
│  ├─ generate_sample_data.py    # Generate synthetic CSV data (large samples)
│  └─ smoke_test_etl.py          # Runs ETL and checks CSV vs DB row counts
├─ data/
│  ├─ raw/
│  │  ├─ sample_data.csv
│  │  └─ sample_data_large.csv
│  └─ processed/
├─ docs/
│  └─ README.md                  # Project docs (short)
├─ results/
│  └─ (output databases go here)
├─ tests/
│  └─ test_etl.py                # pytest tests (transform + CLI integration)
└─ requirements.txt              # dev/test deps (pytest)
```

---

## Quick start

[![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml)
[![Benchmark](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/<OWNER>/<REPO>/main/01_Simple_ETL_CSV_to_DB/results/benchmark_status.json)](01_Simple_ETL_CSV_to_DB/results/benchmark_results.csv)


1. (Optional) Create & activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install test/dev dependencies:

```bash
pip install -r requirements.txt
```

3. Generate a large sample CSV (100k rows by default):

```bash
python code/generate_sample_data.py --rows 100000
```

4. Run the benchmark to compare throughput for different `--batch-sizes` (writes `results/benchmark_results.csv`):

```bash
python code/benchmark_etl.py --batch-sizes 500 1000 5000 10000 --repeats 3 --fast
```

Note: Replace `<OWNER>/<REPO>` in the CI badge URL with your repository path to enable the badge link.
4. Run the ETL (example with batching and fast mode):

```bash
python code/etl_pipeline.py \
  --input data/raw/sample_data_large.csv \
  --db results/output_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

5. Run the smoke test (runs ETL on `sample_data_large.csv` and asserts row counts match):

```bash
python code/smoke_test_etl.py
```

---

## CLI options (for `etl_pipeline.py`)

- `--input, -i` : Input CSV path (default `data/raw/sample_data.csv`)
- `--db` : Output SQLite DB path (default `results/output.db`)
- `--batch-size N` : Rows per DB transaction (default `1000`)
- `--progress N` : Print progress every N rows (0 disables) (default `10000`)
- `--create-index` : Create an index on the `name` column after loading
- `--fast` : Apply PRAGMA optimizations (`WAL`, `synchronous=OFF`) for faster bulk inserts (reduces durability guarantees)

---

## Testing & CI

- Unit and integration tests are in `tests/` and run with `pytest`.
- A GitHub Actions workflow (`.github/workflows/ci.yml`) runs tests on push and pull requests.

Run tests locally:

```bash
pytest -q
```

---

## Notes & recommendations

- The ETL streams the CSV and inserts in batches to keep memory usage low for large inputs.
- Use `--fast` for speed when you can tolerate reduced durability during bulk loads; otherwise omit it for safer commits.
- For production scenarios, consider using a proper RDBMS, add retries and more extensive logging, and add schema/versioning.

---

## Contributing

Contributions welcome — open issues or PRs with improvements, tests, or docs.

---

License: MIT (add license file if you want to publish)

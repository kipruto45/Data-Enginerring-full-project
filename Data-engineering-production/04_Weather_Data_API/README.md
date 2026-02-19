# 04_Weather_Data_API

**Streaming ETL for weather observations: CSV → SQLite**

This project demonstrates a robust ETL pipeline that reads weather observation data from CSV files, applies minimal transformations, and writes results to SQLite with optional performance optimizations. The pipeline supports batching, progress tracking, PRAGMA optimizations, and automatic retries.

---

## Project layout

```
04_Weather_Data_API/
├─ code/
│  ├─ weather_etl_pipeline.py    # Main streaming ETL (batching, PRAGMA, retries, progress)
│  ├─ weather_etl.py             # Placeholder API ETL (example summary generator)
│  └─ generate_weather_data.py   # Generate synthetic weather CSV (large samples)
├─ data/
│  ├─ raw/
│  │  └─ weather_observations_large.csv   # 100k+ observations
│  └─ processed/
├─ docs/
│  └─ README.md
├─ results/
│  └─ (output databases and summaries)
├─ tests/
│  ├─ test_smoke_weather.py      # Smoke tests (CSV row count validation)
│  └─ test_weather_etl_pipeline.py # Unit tests (small CSV load verification)
└─ requirements.txt              # Dependencies (sqlite3 built-in)
```

---

## Quick start

1. Generate a large sample weather CSV (100k rows):

```bash
python code/generate_weather_data.py --rows 100000
```

2. Run the streaming ETL pipeline (batching + PRAGMA optimizations):

```bash
python code/weather_etl_pipeline.py \
  --input data/raw/weather_observations_large.csv \
  --db results/weather_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

Expected output: ~100k rows loaded in ~1 second (progress every 5k rows logged).

3. Run the placeholder weather summary ETL (example):

```bash
python code/weather_etl.py
```

Output: `results/weather_summary.csv`

4. Run smoke tests:

```bash
python -m pytest tests/test_smoke_weather.py -v
```

Verifies: 100k-row CSV exists and has correct line count (100001: header + 100k rows).

5. Run pipeline unit tests:

```bash
python -m pytest tests/test_weather_etl_pipeline.py -v
```

Verifies: streaming load of small CSVs (2 rows) into SQLite tables.

---

## CLI options (`weather_etl_pipeline.py`)

- `--input, -i` : Input CSV path (default `data/raw/weather_observations_large.csv`)
- `--db` : Output SQLite DB path (default `results/weather.db`)
- `--batch-size N` : Rows per transaction (default `5000`)
- `--progress N` : Log progress every N rows (0 disables) (default `20000`)
- `--fast` : Enable PRAGMA optimizations (WAL, synchronous=OFF) for faster bulk inserts
- `--max-retries N` : Retry attempts on DB OperationalError (default `3`)
- `--retry-delay S` : Delay between retries in seconds (default `0.25`)
- `--log-level` : Logging level (DEBUG, INFO, WARNING, ERROR) (default `INFO`)

---

## CSV Format

Expected columns in input CSV:
- `obs_id` (integer, primary key)
- `station` (text)
- `date` (text, ISO format)
- `temp_c` (float, temperature Celsius)
- `condition` (text, e.g., "Sunny", "Cloudy")
- `humidity` (integer, 0-100)

Example row:
```
obs_id,station,date,temp_c,condition,humidity
1,StationA,2021-01-01 12:00:00,20.5,Sunny,65
```

---

## Performance

Loading 100k weather observations on typical hardware:
- Batch size 5000: ~1 second with `--fast` mode
- Throughput: ~100k rows/sec

---

## Notes

- `weather_etl.py` is a placeholder; replace `fetch_weather()` with real API calls (e.g., OpenWeatherMap, NOAA).
- `--fast` mode uses `PRAGMA journal_mode=WAL` and `synchronous=OFF` for speed; use only for data loads where brief durability loss is acceptable.
- Retries are automatic for transient DB errors.

---

## See also

- [Project 01: Simple ETL](../01_Simple_ETL_CSV_to_DB/README.md) – Base ETL pattern
- [Project 03: SQL Aggregation](../03_SQL_Data_Aggregation/README.md) – Query examples

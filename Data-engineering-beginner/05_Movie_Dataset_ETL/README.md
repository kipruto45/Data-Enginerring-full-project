# 05_Movie_Dataset_ETL

**Streaming ETL for movie datasets: CSV → SQLite**

This project demonstrates a scalable ETL pipeline for movie data that reads CSV files, applies transformations, and writes to SQLite. The pipeline includes batching, progress tracking, optional PRAGMA optimizations, and automatic retries for reliability.

---

## Project layout

```
05_Movie_Dataset_ETL/
├─ code/
│  ├─ movie_etl_pipeline.py      # Main streaming ETL (batching, PRAGMA, retries, progress)
│  ├─ movie_etl.py               # Genre aggregation (example: top genres summary)
│  └─ generate_movies_data.py    # Generate synthetic movie CSV (large samples)
├─ data/
│  ├─ raw/
│  │  └─ movies_large.csv        # 100k+ movies
│  └─ processed/
├─ docs/
│  └─ README.md
├─ results/
│  └─ (output databases and summaries)
├─ tests/
│  ├─ test_smoke_movies.py       # Smoke tests (CSV row count validation)
│  └─ test_movie_etl_pipeline.py # Unit tests (small CSV load verification)
└─ requirements.txt              # Dependencies (sqlite3 built-in)
```

---

## Quick start

1. Generate a large sample movie CSV (100k rows):

```bash
python code/generate_movies_data.py --rows 100000
```

2. Run the streaming ETL pipeline (batching + PRAGMA optimizations):

```bash
python code/movie_etl_pipeline.py \
  --input data/raw/movies_large.csv \
  --db results/movies_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

Expected output: ~100k rows loaded in ~1 second (progress logged every 5k rows).

3. Run the example genre aggregation ETL:

```bash
python code/movie_etl.py
```

Output: `results/movies_summary.csv` (top 10 genres with counts).

4. Run smoke tests:

```bash
python -m pytest tests/test_smoke_movies.py -v
```

Verifies: 100k-row CSV exists and has correct line count (100001: header + 100k rows).

5. Run pipeline unit tests:

```bash
python -m pytest tests/test_movie_etl_pipeline.py -v
```

Verifies: streaming load of small CSVs (2 rows) into SQLite tables.

---

## CLI options (`movie_etl_pipeline.py`)

- `--input, -i` : Input CSV path (default `data/raw/movies_large.csv`)
- `--db` : Output SQLite DB path (default `results/movies.db`)
- `--batch-size N` : Rows per transaction (default `5000`)
- `--progress N` : Log progress every N rows (0 disables) (default `20000`)
- `--fast` : Enable PRAGMA optimizations (WAL, synchronous=OFF) for faster bulk inserts
- `--max-retries N` : Retry attempts on DB OperationalError (default `3`)
- `--retry-delay S` : Delay between retries in seconds (default `0.25`)
- `--log-level` : Logging level (DEBUG, INFO, WARNING, ERROR) (default `INFO`)

---

## CSV Format

Expected columns in input CSV:
- `movie_id` (integer, primary key)
- `title` (text)
- `year` (integer)
- `genre` (text, genres separated by `|` for multiple)
- `rating` (float, 0.0–10.0)
- `revenue_millions` (float)

Example row:
```
movie_id,title,year,genre,rating,revenue_millions
1,Inception,2010,Action|Sci-Fi,8.8,839.5
```

---

## Performance

Loading 100k movies on typical hardware:
- Batch size 5000: ~1 second with `--fast` mode
- Throughput: ~100k rows/sec

---

## Notes

- `movie_etl.py` demonstrates genre aggregation; extend with additional analysis (ratings distribution, revenue trends, etc.).
- `--fast` mode uses `PRAGMA journal_mode=WAL` and `synchronous=OFF` for speed; use only for bulk loads where brief durability loss is acceptable.
- Automatic retries handle transient DB errors (e.g., lock contention).

---

## See also

- [Project 01: Simple ETL](../01_Simple_ETL_CSV_to_DB/README.md) – Base ETL pattern
- [Project 03: SQL Aggregation](../03_SQL_Data_Aggregation/README.md) – Query examples

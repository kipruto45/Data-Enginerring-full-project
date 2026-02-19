# 05_Movie_Dataset_ETL

Starter movie ETL project that aggregates genres from a raw CSV and writes a summary output.

## What This Project Demonstrates

- Reading structured CSV input with `csv.DictReader`
- Lightweight transformation (genre tokenization)
- Basic aggregation with `collections.Counter`
- Writing summarized output to CSV

## Input Requirement

Place a `movies.csv` file at:

- `data/raw/movies.csv`

Expected key column:

- `genre` (pipe-separated genres, for example `Action|Sci-Fi`)

## Run

```bash
python code/movie_etl.py
```

## Output

- `results/movies_summary.csv` containing `genre,count`

## Note

For a complete scalable pipeline version with large-data generation, SQLite loading, and tests, use `Data-engineering-beginner/05_Movie_Dataset_ETL`.

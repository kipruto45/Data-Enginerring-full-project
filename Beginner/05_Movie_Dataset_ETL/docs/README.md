# 05_Movie_Dataset_ETL

Operational notes for the starter movie ETL script.

## Run Script

```bash
python code/movie_etl.py
```

## Required Input

- `data/raw/movies.csv`
- Column `genre` with `|`-separated values

## Produced Output

- `results/movies_summary.csv`

## Typical Extension Points

- Add more fields (rating, revenue, release year)
- Add filtering and data-quality checks
- Persist detailed rows to SQLite

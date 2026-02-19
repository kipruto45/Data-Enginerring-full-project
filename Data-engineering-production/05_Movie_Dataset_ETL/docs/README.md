# 05_Movie_Dataset_ETL

Runbook for movie ETL pipeline operations.

## Generate Input Data

```bash
python code/generate_movies_data.py --rows 50000 --out data/raw/movies_large.csv
```

## Run ETL

```bash
python code/movie_etl_pipeline.py \
  --input data/raw/movies_large.csv \
  --db results/movies_large.db \
  --batch-size 5000 \
  --progress 20000 \
  --fast
```

## Validate

```bash
pytest -q tests
```

## Output Tables

- `movies` (in SQLite DB): loaded movie records

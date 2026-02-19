# 02_CSV_Excel_Cleaning

Reference guide for the full cleaning workflow.

## Generate Sample Input

```bash
python code/generate_sample_csv.py --rows 50000 --out data/raw/sample_large.csv
```

## Run Cleaning

```bash
python code/cleaning_script.py \
  --input data/raw/sample_large.csv \
  --output data/cleaned/cleaned_large.csv \
  --remove-duplicates \
  --fill-na-numeric 0 \
  --fill-na-string Unknown
```

## CLI Highlights

- `--input`, `--output`
- `--drop-empty-rows`, `--drop-empty-cols`
- `--fill-na-numeric`, `--fill-na-string`
- `--strip-whitespace`, `--remove-duplicates`
- `--profile`, `--log-level`

## Validation

```bash
pytest -q tests
```

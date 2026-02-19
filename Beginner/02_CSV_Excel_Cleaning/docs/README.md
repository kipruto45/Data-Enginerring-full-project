# 02_CSV_Excel_Cleaning

CSV and Excel data cleaning utilities with CLI options and unit tests.

## Quick start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the cleaning script on a sample CSV:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/cleaned.csv
```

## CLI options

- `--input, -i` : Input CSV/XLSX path (default: `data/raw/sample.csv`)
- `--output, -o` : Output CSV path (default: `data/cleaned/cleaned_sample.csv`)
- `--drop-empty-rows` : Remove rows where all values are NaN (default: True)
- `--drop-empty-cols` : Remove columns where all values are NaN (default: False)
- `--fill-na-numeric FLOAT` : Fill NaN in numeric columns with this value
- `--fill-na-string STR` : Fill NaN in string columns with this value
- `--strip-whitespace` : Strip leading/trailing whitespace from strings (default: True)
- `--remove-duplicates` : Remove duplicate rows (default: False)
- `--log-level LEVEL` : Logging level (DEBUG, INFO, WARNING, ERROR) (default: INFO)
- `--profile` : Print data profile before/after cleaning

## Examples

Remove empty rows and duplicates:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/clean.csv --remove-duplicates
```

Fill NaN values:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/clean.csv --fill-na-numeric 0 --fill-na-string "Unknown"
```

Profile the data:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --profile
```

## Testing

Run unit tests:
```bash
pytest -q tests/
```

## Notes

- The script preserves column order and index (unless `remove-duplicates` is used).
- For large files (GB+), consider processing in chunks or using `pandas.read_csv(..., chunksize=N)`.

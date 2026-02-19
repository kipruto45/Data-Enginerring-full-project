# 02_CSV_Excel_Cleaning

**CSV and Excel data cleaning utilities** with configurable cleaning rules, CLI options, logging, and tests.

## Project layout

```
02_CSV_Excel_Cleaning/
├─ code/
│  └─ cleaning_script.py           # Main cleaning utility (CLI + options)
├─ data/
│  ├─ raw/
│  │  └─ sample.csv                # Small sample input
│  └─ cleaned/                     # Output directory
├─ docs/
│  └─ README.md                    # Short docs
├─ tests/
│  └─ test_cleaning.py             # pytest tests
├─ results/                        # (for optional outputs)
└─ requirements.txt                # pandas, openpyxl, pytest
```

## Quick start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Basic cleaning:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/cleaned.csv
```

3. Run tests:
```bash
pytest -q tests/
```

## Features

- **Flexible cleaning**: drop empty rows/cols, fill NaNs, strip whitespace, remove duplicates
- **CLI options**: configure each operation via command-line flags
- **Logging**: structured logs with data profiling (before/after row/col counts, dtypes)
- **Error handling**: graceful failures with clear messages
- **Tests**: unit tests for key operations (empty row removal, whitespace stripping, error cases)

## CLI Examples

Drop empty rows + remove duplicates:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/clean.csv --remove-duplicates
```

Fill missing values:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/clean.csv --fill-na-numeric 0 --fill-na-string "Unknown"
```

Profile before/after:
```bash
python code/cleaning_script.py --input data/raw/sample.csv --profile
```

## Notes

- Supports both CSV (`.csv`) and Excel (`.xlsx`) input files
- Output is always CSV
- For very large files, consider reading in chunks: `pd.read_csv(path, chunksize=10000)`

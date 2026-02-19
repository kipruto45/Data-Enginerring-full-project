# 02_CSV_Excel_Cleaning

A configurable data-cleaning utility for CSV/XLSX files using pandas.

## Capabilities

- Drop empty rows and optional empty columns
- Strip whitespace from string fields
- Fill missing numeric and string values
- Remove duplicate rows
- Optional before/after profiling logs

## Project Structure

```text
02_CSV_Excel_Cleaning/
├── code/cleaning_script.py
├── data/raw/sample.csv
├── docs/README.md
├── tests/test_cleaning.py
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python code/cleaning_script.py \
  --input data/raw/sample.csv \
  --output data/cleaned/cleaned_sample.csv
```

## Common Examples

```bash
python code/cleaning_script.py --remove-duplicates --profile
```

```bash
python code/cleaning_script.py \
  --fill-na-numeric 0 \
  --fill-na-string Unknown
```

## Testing

```bash
pytest -q tests
```

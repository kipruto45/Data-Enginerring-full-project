# 02_CSV_Excel_Cleaning

A production-friendly cleaning pipeline for CSV/XLSX datasets with synthetic data generation and automated tests.

## Capabilities

- Configurable cleaning operations from CLI
- Built-in synthetic data generator for performance testing
- Structured logs and optional profile output
- Unit tests for cleaning behavior

## Project Structure

```text
02_CSV_Excel_Cleaning/
├── code/
│   ├── cleaning_script.py
│   └── generate_sample_csv.py
├── data/raw/
├── docs/README.md
├── tests/test_cleaning.py
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
python code/generate_sample_csv.py --rows 100000 --out data/raw/sample_large.csv
python code/cleaning_script.py --input data/raw/sample_large.csv --output data/cleaned/cleaned_large.csv
```

## Testing

```bash
pytest -q tests
```

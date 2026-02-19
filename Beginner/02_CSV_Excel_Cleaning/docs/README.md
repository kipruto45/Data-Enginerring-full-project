# 02_CSV_Excel_Cleaning

Operational notes for the cleaning utility.

## CLI Flags

- `--input, -i`: Input CSV/XLSX path
- `--output, -o`: Output CSV path
- `--drop-empty-rows`: Drop rows with all fields empty
- `--drop-empty-cols`: Drop columns with all fields empty
- `--fill-na-numeric`: Fill missing numeric values
- `--fill-na-string`: Fill missing string values
- `--strip-whitespace`: Trim whitespace from string values
- `--remove-duplicates`: Remove duplicate rows
- `--profile`: Log basic profile information
- `--log-level`: Logging level

## Example Commands

```bash
python code/cleaning_script.py --input data/raw/sample.csv --output data/cleaned/clean.csv
```

```bash
python code/cleaning_script.py --profile --remove-duplicates
```

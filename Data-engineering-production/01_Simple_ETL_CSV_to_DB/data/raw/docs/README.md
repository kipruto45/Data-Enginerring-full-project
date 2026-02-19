# Raw Input Data

This folder stores source CSV files used by `01_Simple_ETL_CSV_to_DB`.

## Expected Files

- `sample_data.csv` - small default dataset
- `sample_data_large.csv` - large dataset for benchmarking and smoke tests

## Regenerate Sample Data

From the project root:

```bash
python code/generate_sample_data.py --rows 100000 --out data/raw/sample_data_large.csv
```

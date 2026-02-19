"""CSV and Excel cleaning starter script

Usage:
    python cleaning_script.py --input data/raw/sample.csv --output data/cleaned/cleaned.csv

Note: this script demonstrates basic cleaning. Extend with domain-specific rules as needed.
"""

import pandas as pd
import argparse
import logging
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_CSV = ROOT / "data" / "raw" / "sample.csv"
DEFAULT_OUT = ROOT / "data" / "cleaned" / "cleaned_sample.csv"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("cleaning")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="Clean CSV/Excel files")
    p.add_argument("--input", "-i", default=str(DEFAULT_RAW_CSV), help="Input CSV/XLSX path")
    p.add_argument("--output", "-o", default=str(DEFAULT_OUT), help="Output CSV path")
    p.add_argument("--drop-empty-rows", action="store_true", default=True, help="Drop rows where all values are NaN")
    p.add_argument("--drop-empty-cols", action="store_true", default=False, help="Drop columns where all values are NaN")
    p.add_argument("--fill-na-numeric", type=float, default=None, help="Fill NaN in numeric columns with this value")
    p.add_argument("--fill-na-string", type=str, default=None, help="Fill NaN in string columns with this value")
    p.add_argument("--strip-whitespace", action="store_true", default=True, help="Strip leading/trailing whitespace from strings")
    p.add_argument("--remove-duplicates", action="store_true", default=False, help="Remove duplicate rows")
    p.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    p.add_argument("--profile", action="store_true", help="Print data profile (count, dtype, nulls) before/after")
    return p.parse_args()


def load(path, logger=None):
    """Load CSV or Excel file with error handling."""
    try:
        if logger:
            logger.info(f"Loading {path}")
        if str(path).endswith(".xlsx"):
            return pd.read_excel(path)
        else:
            return pd.read_csv(path)
    except Exception as e:
        if logger:
            logger.error(f"Failed to load {path}: {e}")
        raise


def get_profile(df, name=""):
    """Return a simple data profile dict."""
    return {
        "name": name,
        "rows": len(df),
        "cols": len(df.columns),
        "dtypes": df.dtypes.value_counts().to_dict(),
        "nulls": df.isnull().sum().to_dict()
    }


def clean(df, drop_empty_rows=True, drop_empty_cols=False, fill_na_numeric=None, fill_na_string=None, strip_whitespace=True, remove_duplicates=False, logger=None):
    """Apply cleaning operations to dataframe."""
    if logger:
        prof_before = get_profile(df, "before")
        logger.info(f"Before: {prof_before['rows']} rows, {prof_before['cols']} cols")
    
    # drop entirely empty rows
    if drop_empty_rows:
        df = df.dropna(how="all")
        if logger:
            logger.info("Dropped empty rows")
    
    # drop entirely empty columns
    if drop_empty_cols:
        df = df.dropna(axis=1, how="all")
        if logger:
            logger.info("Dropped empty columns")
    
    # strip column names
    df.columns = [c.strip() for c in df.columns]
    
    # strip whitespace from string columns
    if strip_whitespace:
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].str.strip()
        if logger:
            logger.info("Stripped whitespace from string columns")
    
    # fill NaNs
    if fill_na_numeric is not None:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col].fillna(fill_na_numeric, inplace=True)
        if logger:
            logger.info(f"Filled {len(numeric_cols)} numeric columns with {fill_na_numeric}")
    if fill_na_string is not None:
        string_cols = df.select_dtypes(include=["object"]).columns
        for col in string_cols:
            df[col].fillna(fill_na_string, inplace=True)
        if logger:
            logger.info(f"Filled {len(string_cols)} string columns with '{fill_na_string}'")
    
    # remove duplicates
    if remove_duplicates:
        before_dup = len(df)
        df = df.drop_duplicates()
        if logger:
            logger.info(f"Removed {before_dup - len(df)} duplicate rows")
    
    if logger:
        prof_after = get_profile(df, "after")
        logger.info(f"After: {prof_after['rows']} rows, {prof_after['cols']} cols")
    
    return df


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    try:
        path = Path(args.input)
        if not path.exists():
            logger.error(f"Input file not found: {path}")
            raise SystemExit(1)
        
        df = load(path, logger=logger)
        df = clean(df, drop_empty_rows=args.drop_empty_rows, drop_empty_cols=args.drop_empty_cols, fill_na_numeric=args.fill_na_numeric, fill_na_string=args.fill_na_string, strip_whitespace=args.strip_whitespace, remove_duplicates=args.remove_duplicates, logger=logger)
        
        # create output directory if needed
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
        logger.info(f"Cleaned data written to {out_path}")
        
        if args.profile:
            prof = get_profile(df, "final")
            logger.info(f"Profile: {json.dumps(prof, default=str)}")
    except Exception as e:
        logger.exception("Cleaning failed")
        raise

"""Generate synthetic CSV data for ETL testing

Usage:
    python generate_sample_data.py --rows 100000 --out ../data/raw/sample_data_large.csv
"""

import csv
import random
import argparse
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "raw" / "sample_data_large.csv"

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]


def random_name():
    return random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES)


def random_date(start_year=2020, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    days = (end - start).days
    return (start + timedelta(days=random.randint(0, days))).isoformat()


def generate(path, rows=100000):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "value", "category", "date"])
        for i in range(rows):
            name = random_name()
            value = round(random.random() * 1000, 2)
            category = random.choice(["A", "B", "C", "D"])
            d = random_date()
            writer.writerow([name, value, category, d])
    print(f"Wrote {rows} rows to {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=100000, help="Number of rows to generate")
    p.add_argument("--out", type=str, default=str(DEFAULT_OUT), help="Output CSV path")
    args = p.parse_args()
    generate(args.out, args.rows)

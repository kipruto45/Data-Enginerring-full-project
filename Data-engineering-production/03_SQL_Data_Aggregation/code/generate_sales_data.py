"""Generate synthetic sales CSV for aggregation tests

Usage:
    python generate_sales_data.py --rows 100000 --out ../data/raw/sales_data_large.csv
"""

import csv
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "raw" / "sales_data_large.csv"

REGIONS = ["North","South","East","West","Central"]
PRODUCTS = ["Widget","Gadget","Doohickey","Thingamajig","Whatsit"]


def generate(out_path, rows=100000):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2020,1,1)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sale_id","date","region","product","quantity","amount"])
        for i in range(rows):
            date = start + timedelta(days=random.randint(0, 365*3))
            region = random.choice(REGIONS)
            product = random.choice(PRODUCTS)
            q = random.randint(1,20)
            amount = round(q * random.uniform(5.0, 500.0),2)
            writer.writerow([i+1, date.strftime("%Y-%m-%d"), region, product, q, amount])
    print(f"Wrote {rows} rows to {out}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--rows', type=int, default=100000)
    p.add_argument('--out', type=str, default=str(DEFAULT_OUT))
    args = p.parse_args()
    generate(args.out, args.rows)

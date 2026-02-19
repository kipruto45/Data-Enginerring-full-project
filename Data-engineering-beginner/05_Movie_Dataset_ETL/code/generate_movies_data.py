"""Generate synthetic movie dataset CSV

Usage:
    python generate_movies_data.py --rows 100000 --out ../data/raw/movies_large.csv
"""

import csv
import random
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "raw" / "movies_large.csv"

GENRES = ["Drama","Comedy","Action","Thriller","Romance","Sci-Fi","Documentary","Horror"]


def title(i):
    adj = ["Dark","Bright","Final","Hidden","Lost","Last","First","New","Old","Silent"]
    noun = ["Night","Day","City","Hero","Dream","Secret","Memory","World","Game","Light"]
    return f"{random.choice(adj)} {random.choice(noun)} {i}"


def generate(out_path, rows=100000):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["movie_id","title","year","genre","rating","revenue_millions"])
        for i in range(rows):
            yr = random.randint(1950,2024)
            g = random.choice(GENRES)
            r = round(random.uniform(1.0,10.0),1)
            rev = round(random.uniform(0.1,500.0),2)
            writer.writerow([i+1, title(i+1), yr, g, r, rev])
    print(f"Wrote {rows} rows to {out}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--rows', type=int, default=100000)
    p.add_argument('--out', type=str, default=str(DEFAULT_OUT))
    args = p.parse_args()
    generate(args.out, args.rows)

"""Generate synthetic CSV data for cleaning tests

Usage:
    python generate_sample_csv.py --rows 100000 --out ../data/raw/sample_large.csv
"""

import csv
import random
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "raw" / "sample_large.csv"

FIRST = ["Alice","Bob","Charlie","Diana","Eve","Frank","Grace","Heidi","Ivan","Judy"]
LAST = ["Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia","Rodriguez","Wilson"]


def gen_name():
    # include some whitespace/noise
    name = random.choice(FIRST) + " " + random.choice(LAST)
    if random.random() < 0.1:
        return "  " + name + "  "
    return name


def gen_age():
    if random.random() < 0.02:
        return ""
    return random.randint(18, 80)


def generate(path, rows=100000):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","name","age","score"])
        for i in range(rows):
            name = gen_name()
            age = gen_age()
            score = round(random.random()*100,2) if random.random() > 0.05 else ""
            writer.writerow([i+1, name, age, score])
    print(f"Wrote {rows} rows to {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, default=100000)
    p.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = p.parse_args()
    generate(args.out, args.rows)

"""Movie dataset ETL starter

This script shows how to read movie CSV, do a simple aggregation, and write a summary.
"""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "movies.csv"
RESULT = ROOT / "results" / "movies_summary.csv"


def top_genres(path=RAW, top_n=10):
    genres = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("genre"):
                for g in r["genre"].split("|"):
                    genres.append(g.strip())
    return Counter(genres).most_common(top_n)


if __name__ == "__main__":
    if not RAW.exists():
        print("No movies.csv found in data/raw/. Add one or export from public datasets.")
    else:
        top = top_genres()
        with open(RESULT, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["genre", "count"])
            writer.writerows(top)
        print(f"Wrote summary to {RESULT}")

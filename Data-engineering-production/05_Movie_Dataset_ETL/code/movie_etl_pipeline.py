"""Streaming ETL for Movie dataset

Usage:
    python movie_etl_pipeline.py --input data/raw/movies_large.csv --db results/movies.db --batch-size 5000 --progress 20000 --fast
"""

import csv
import sqlite3
import time
import argparse
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "movies_large.csv"
DEFAULT_DB = ROOT / "results" / "movies.db"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("movie_etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="Movie CSV -> SQLite ETL")
    p.add_argument("--input", "-i", default=str(DEFAULT_CSV))
    p.add_argument("--db", default=str(DEFAULT_DB))
    p.add_argument("--batch-size", type=int, default=5000)
    p.add_argument("--progress", type=int, default=20000)
    p.add_argument("--fast", action="store_true", help="Enable PRAGMA optimizations (WAL, synchronous=OFF)")
    p.add_argument("--max-retries", type=int, default=3)
    p.add_argument("--retry-delay", type=float, default=0.25)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()


def extract(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def transform_row(r):
    return {
        "movie_id": int(r.get("movie_id") or 0),
        "title": (r.get("title") or "").strip(),
        "year": int(r.get("year") or 0),
        "genre": (r.get("genre") or "").strip(),
        "rating": float(r.get("rating") or 0.0),
        "revenue_millions": float(r.get("revenue_millions") or 0.0)
    }


def load(rows, db_path, batch_size=5000, max_retries=3, retry_delay=0.25, fast=False, logger=None):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    attempts = 0
    while True:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            if fast:
                cur.execute("PRAGMA journal_mode=WAL;")
                cur.execute("PRAGMA synchronous=OFF;")
            cur.execute("CREATE TABLE IF NOT EXISTS movies (movie_id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, rating REAL, revenue_millions REAL)")

            batch = []
            inserted = 0
            start = time.time()
            for r in rows:
                batch.append((r["movie_id"], r["title"], r["year"], r["genre"], r["rating"], r["revenue_millions"]))
                if len(batch) >= batch_size:
                    cur.executemany("INSERT OR REPLACE INTO movies (movie_id, title, year, genre, rating, revenue_millions) VALUES (?, ?, ?, ?, ?, ?)", batch)
                    conn.commit()
                    inserted += len(batch)
                    batch = []
                    if logger:
                        logger.info(f"progress: inserted={inserted} elapsed_s={time.time()-start:.2f}")
            if batch:
                cur.executemany("INSERT OR REPLACE INTO movies (movie_id, title, year, genre, rating, revenue_millions) VALUES (?, ?, ?, ?, ?, ?)", batch)
                conn.commit()
                inserted += len(batch)
            if logger:
                logger.info(f"load_complete: total_inserted={inserted} elapsed_s={time.time()-start:.2f}")
            conn.close()
            return inserted
        except sqlite3.OperationalError as e:
            attempts += 1
            if attempts > max_retries:
                if logger:
                    logger.error(f"DB load failed after {attempts} attempts: {e}")
                raise
            if logger:
                logger.warning(f"DB load failed (attempt {attempts}), retrying in {retry_delay}s: {e}")
            time.sleep(retry_delay)


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    csv_path = Path(args.input)
    if not csv_path.exists():
        logger.error(f"Input CSV not found: {csv_path}")
        raise SystemExit(1)

    rows = (transform_row(r) for r in extract(csv_path))
    total = load(rows, args.db, batch_size=args.batch_size, max_retries=args.max_retries, retry_delay=args.retry_delay, fast=args.fast, logger=logger)
    logger.info(f"Finished: loaded {total} rows into {args.db}")
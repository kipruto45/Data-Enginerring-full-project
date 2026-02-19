"""Simple ETL: CSV to SQLite example

This is a lightweight starter ETL script intended for learning.

Usage:
    python etl_pipeline.py

It will: read `data/raw/sample_data.csv`, do a tiny cleaning step, and store results
in `results/output.db` into table `sample`.
"""

import csv
import sqlite3
import argparse
import logging
import json
import time
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT / "data" / "raw" / "sample_data.csv"
DB = ROOT / "results" / "output.db"


class JSONFormatter(logging.Formatter):
    def format(self, record):
        # Basic JSON-formatted logs with timestamp, level, and message
        data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # include any extra fields provided via 'extra' kwarg
        extra = {k: v for k, v in record.__dict__.items() if k not in ("name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process")}
        if extra:
            data["extra"] = extra
        return json.dumps(data, default=str)


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", default=str(DEFAULT_RAW), help="Input CSV path")
    p.add_argument("--db", default=str(DB), help="Output SQLite DB path")
    p.add_argument("--batch-size", type=int, default=1000, help="Number of rows to insert per DB transaction")
    p.add_argument("--progress", type=int, default=10000, help="Print progress every N rows (0 to disable)")
    p.add_argument("--create-index", action="store_true", help="Create index on name after loading")
    p.add_argument("--fast", action="store_true", help="Enable PRAGMA optimizations for faster bulk inserts (may affect durability)")
    p.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    p.add_argument("--max-retries", type=int, default=5, help="Max retries for transient DB errors")
    p.add_argument("--retry-delay", type=float, default=0.1, help="Base retry delay in seconds (exponential backoff applied)")
    return p.parse_args()

def extract(path, logger=None):
    """Stream rows from CSV as dicts (generator)."""
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                yield r
    except Exception as e:
        if logger:
            logger.error("Failed to read CSV", extra={"error": str(e), "path": str(path)})
        raise


def transform_row(r):
    # trivial transform: strip whitespace and title-case column 'name' if present
    try:
        if "name" in r and r.get("name") is not None:
            r["name"] = r["name"].strip().title()
        return r
    except Exception:
        # Log and return the row unchanged to avoid crashing the pipeline
        logging.getLogger("etl").exception("Transform failed for row", extra={"row": r})
        return r


def load(rows, db_path=DB, batch_size=1000, progress_interval=0, create_index=False, fast=False, max_retries=5, retry_delay=0.1, logger=None):
    start_time = time.monotonic()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if fast:
        # speed up bulk inserts (risk: durability/atomicity during crash) - optional
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=OFF")
    cur.execute("CREATE TABLE IF NOT EXISTS sample (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
    to_insert = []
    total = 0
    last_report = start_time
    for r in rows:
        # ensure value is numeric
        try:
            val = float(r.get("value", 0))
        except Exception:
            val = 0.0
        to_insert.append((r.get("name"), val))
        if len(to_insert) >= batch_size:
            # attempt to write batch with retries on OperationalError
            attempt = 0
            while True:
                try:
                    cur.executemany("INSERT INTO sample (name, value) VALUES (?, ?)", to_insert)
                    conn.commit()
                    break
                except sqlite3.OperationalError as e:
                    attempt += 1
                    if attempt > max_retries:
                        if logger:
                            logger.error("Max retries exceeded during DB write", extra={"error": str(e)})
                        raise
                    sleep_time = retry_delay * (2 ** (attempt - 1)) + random.random() * retry_delay
                    if logger:
                        logger.warning("DB write failed, retrying", extra={"attempt": attempt, "sleep": sleep_time, "error": str(e)})
                    time.sleep(sleep_time)
            total += len(to_insert)
            now = time.monotonic()
            if progress_interval and total % progress_interval == 0:
                elapsed = now - start_time
                rate = total / elapsed if elapsed > 0 else 0
                if logger:
                    logger.info("progress", extra={"inserted": total, "elapsed_s": round(elapsed, 2), "rows_per_s": round(rate, 2)})
                else:
                    print(f"Inserted {total} rows ({round(rate,2)} rows/s)")
            to_insert = []
    # insert any remaining
    if to_insert:
        attempt = 0
        while True:
            try:
                cur.executemany("INSERT INTO sample (name, value) VALUES (?, ?)", to_insert)
                conn.commit()
                break
            except sqlite3.OperationalError as e:
                attempt += 1
                if attempt > max_retries:
                    if logger:
                        logger.error("Max retries exceeded during DB write", extra={"error": str(e)})
                    raise
                sleep_time = retry_delay * (2 ** (attempt - 1)) + random.random() * retry_delay
                if logger:
                    logger.warning("DB write failed, retrying", extra={"attempt": attempt, "sleep": sleep_time, "error": str(e)})
                time.sleep(sleep_time)
        total += len(to_insert)
    # create index if requested
    if create_index:
        if logger:
            logger.info("Creating index on sample(name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sample_name ON sample (name)")
        conn.commit()
    conn.close()
    elapsed_total = time.monotonic() - start_time
    if logger:
        logger.info("load_complete", extra={"total_inserted": total, "elapsed_s": round(elapsed_total, 2), "rows_per_s": round(total / elapsed_total if elapsed_total>0 else 0, 2)})
    else:
        print(f"Loaded {total} rows in {round(elapsed_total,2)}s ({round(total/elapsed_total if elapsed_total>0 else 0,2)} rows/s)")
    return total


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    src = Path(args.input)
    try:
        # create an iterator that yields transformed rows
        transformed = (transform_row(r) for r in extract(src, logger=logger))
        total = load(transformed, db_path=args.db, batch_size=args.batch_size, progress_interval=args.progress, create_index=args.create_index, fast=args.fast, max_retries=args.max_retries, retry_delay=args.retry_delay, logger=logger)
        logger.info("finished", extra={"total": total, "db": args.db})
        print(f"Loaded {total} rows into {args.db}")
    except Exception as e:
        logger.exception("ETL failed", extra={"error": str(e)})
        raise

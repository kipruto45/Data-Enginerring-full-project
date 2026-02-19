"""Smoke test: run ETL on the large CSV and verify the DB row count matches."""
import subprocess
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "sample_data_large.csv"
DB = ROOT / "results" / "test_output.db"


def run_etl():
    cmd = ["python3", str(ROOT / "code" / "etl_pipeline.py"), "--input", str(CSV), "--db", str(DB), "--batch-size", "5000", "--progress", "20000"]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def count_db_rows():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sample")
    c = cur.fetchone()[0]
    conn.close()
    return c


def count_csv_rows():
    # subtract one for header
    with open(CSV, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1


if __name__ == "__main__":
    if not CSV.exists():
        raise SystemExit(f"CSV not found: {CSV}")
    if DB.exists():
        DB.unlink()
    run_etl()
    db_count = count_db_rows()
    csv_count = count_csv_rows()
    print(f"CSV rows: {csv_count}; DB rows: {db_count}")
    if db_count != csv_count:
        raise SystemExit("Row count mismatch")
    print("Smoke test passed")

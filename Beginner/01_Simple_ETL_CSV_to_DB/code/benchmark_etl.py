"""Benchmark ETL throughput for different batch sizes.

Example:
    python benchmark_etl.py --csv data/raw/sample_data_large.csv --batch-sizes 500 1000 5000 10000 --repeats 3 --fast

This will run the ETL for each batch size N times and report rows/sec and time.
"""

import argparse
import csv
import subprocess
import time
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "raw" / "sample_data_large.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def count_csv_rows(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1


def run_single(csv_path, db_path, batch_size, fast=False):
    cmd = ["python3", str(ROOT / "code" / "etl_pipeline.py"), "--input", str(csv_path), "--db", str(db_path), "--batch-size", str(batch_size)]
    if fast:
        cmd.append("--fast")
    start = time.monotonic()
    subprocess.check_call(cmd)
    elapsed = time.monotonic() - start
    rows = count_csv_rows(csv_path)
    return elapsed, rows


def benchmark(csv_path, batch_sizes, repeats=3, fast=False):
    results = []
    for bs in batch_sizes:
        times = []
        for r in range(repeats):
            db = RESULTS_DIR / f"benchmark_bs{bs}_run{r}.db"
            if db.exists():
                db.unlink()
            elapsed, rows = run_single(csv_path, db, bs, fast=fast)
            times.append(elapsed)
            print(f"bs={bs} run={r} elapsed={elapsed:.2f}s rows={rows} rate={rows/elapsed:.2f} rows/s")
        results.append({"batch_size": bs, "runs": repeats, "mean_s": statistics.mean(times), "stdev_s": statistics.stdev(times) if len(times)>1 else 0.0, "rows": rows, "rows_per_s": rows / statistics.mean(times)})
    # write CSV
    out = RESULTS_DIR / "benchmark_results.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["batch_size", "runs", "mean_s", "stdev_s", "rows", "rows_per_s"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print(f"Wrote benchmark results to {out}")
    return results


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=str(DEFAULT_CSV), help="CSV input path")
    p.add_argument("--batch-sizes", nargs="+", type=int, default=[500,1000,5000,10000], help="Batch sizes to test")
    p.add_argument("--repeats", type=int, default=3, help="Number of repeats per batch size")
    p.add_argument("--fast", action="store_true", help="Enable PRAGMA optimizations during runs")
    args = p.parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path} (generate with code/generate_sample_data.py)")
    benchmark(csv_path, args.batch_sizes, repeats=args.repeats, fast=args.fast)

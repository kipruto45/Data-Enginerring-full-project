import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "code" / "benchmark_etl.py"
RESULT = ROOT / "results" / "benchmark_results.csv"


def test_benchmark_writes_results(tmp_path):
    # create a small CSV for fast testing
    csv = tmp_path / "small.csv"
    with csv.open("w", encoding="utf-8") as f:
        f.write("name,value,category,date\n")
        for i in range(2000):
            f.write(f"User{i},{i%100},{'A'},2020-01-01\n")
    # ensure old result removed
    if RESULT.exists():
        RESULT.unlink()
    cmd = ["python3", str(BENCH), "--csv", str(csv), "--batch-sizes", "500", "1000", "--repeats", "1"]
    subprocess.check_call(cmd)
    assert RESULT.exists()
    # basic check: file contains header and at least one line
    with RESULT.open() as f:
        lines = f.read().strip().splitlines()
    assert len(lines) >= 2
    assert lines[0].startswith("batch_size")

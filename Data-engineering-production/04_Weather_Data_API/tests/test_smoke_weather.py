import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ETL = ROOT / "code" / "weather_etl.py"
RAW = ROOT / "data" / "raw" / "weather_observations_large.csv"
RESULT = ROOT / "results" / "weather_summary.csv"


def test_weather_large_csv_exists():
    assert RAW.exists()
    # header + 100000 rows expected
    assert sum(1 for _ in RAW.open()) == 100001


def test_weather_etl_runs_and_writes_summary(tmp_path):
    # run the ETL (placeholder)
    subprocess.check_call(["python3", str(ETL)])
    assert RESULT.exists()
    # quick check: file has header
    with RESULT.open() as f:
        assert len(f.readline().strip()) > 0

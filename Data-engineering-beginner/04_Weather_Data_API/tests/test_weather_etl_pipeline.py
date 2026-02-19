import sqlite3
from pathlib import Path
import csv
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ETL = ROOT / "code" / "weather_etl_pipeline.py"


def test_weather_pipeline_small_csv(tmp_path):
    csv_path = tmp_path / "small_weather.csv"
    rows = [
        {"obs_id": "1", "station": "S1", "date": "2021-01-01", "temp_c": "10.0", "condition": "Sunny", "humidity": "50"},
        {"obs_id": "2", "station": "S2", "date": "2021-01-02", "temp_c": "5.0", "condition": "Cloudy", "humidity": "80"},
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    db = tmp_path / "test_weather.db"
    subprocess.check_call(["python3", str(ETL), "--input", str(csv_path), "--db", str(db)])

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM weather")
    count = cur.fetchone()[0]
    conn.close()
    assert count == 2

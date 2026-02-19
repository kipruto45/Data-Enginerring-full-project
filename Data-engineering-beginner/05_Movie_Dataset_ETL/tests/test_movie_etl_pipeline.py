import sqlite3
from pathlib import Path
import csv
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ETL = ROOT / "code" / "movie_etl_pipeline.py"


def test_movie_pipeline_small_csv(tmp_path):
    csv_path = tmp_path / "small_movies.csv"
    rows = [
        {"movie_id": "1", "title": "A", "year": "2000", "genre": "Action", "rating": "7.5", "revenue_millions": "10.0"},
        {"movie_id": "2", "title": "B", "year": "2001", "genre": "Drama", "rating": "8.0", "revenue_millions": "5.0"},
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    db = tmp_path / "test_movies.db"
    subprocess.check_call(["python3", str(ETL), "--input", str(csv_path), "--db", str(db)])

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM movies")
    count = cur.fetchone()[0]
    conn.close()
    assert count == 2

import subprocess
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGG = ROOT / "code" / "aggregation.py"
SAMPLE_CSV = ROOT / "data" / "raw" / "sales_data.csv"


def test_load_csv(tmp_path):
    csv = tmp_path / "sales.csv"
    csv.write_text("date,region,product,amount,quantity\n2026-01-01,North,A,100.00,1\n2026-01-01,South,B,50.00,2\n")
    db = tmp_path / "test.db"
    cmd = ["python3", str(AGG), "--csv", str(csv), "--db", str(db), "--load-csv"]
    subprocess.check_call(cmd)
    # verify DB has rows
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sales")
    count = cur.fetchone()[0]
    conn.close()
    assert count == 2


def test_query_execution(tmp_path):
    # create and load test DB
    csv = tmp_path / "sales.csv"
    csv.write_text("date,region,product,amount,quantity\n2026-01-01,North,A,100.00,1\n2026-01-01,North,B,50.00,2\n2026-01-01,South,A,200.00,1\n")
    db = tmp_path / "test.db"
    cmd = ["python3", str(AGG), "--csv", str(csv), "--db", str(db), "--load-csv"]
    subprocess.check_call(cmd)
    # run query
    cmd = ["python3", str(AGG), "--db", str(db), "--query", "SELECT region, SUM(amount) as total FROM sales GROUP BY region"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

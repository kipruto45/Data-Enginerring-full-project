import importlib.util
import subprocess
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ETL_PATH = ROOT / "code" / "etl_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("etl_pipeline", str(ETL_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_transform_row():
    module = load_module()
    row = {"name": "  alice "}
    out = module.transform_row(row)
    assert out["name"] == "Alice"


def test_cli_load(tmp_path):
    csv = tmp_path / "small.csv"
    csv.write_text("name,value\nAlice,10\nBob,20\n")
    db = tmp_path / "test.db"
    cmd = ["python3", str(ETL_PATH), "--input", str(csv), "--db", str(db), "--batch-size", "1"]
    subprocess.check_call(cmd)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sample")
    c = cur.fetchone()[0]
    conn.close()
    assert c == 2

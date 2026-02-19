import sqlite3
from pathlib import Path
from types import SimpleNamespace

import importlib.util

ROOT = Path(__file__).resolve().parents[1]
ETL_PATH = ROOT / "code" / "etl_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("etl_pipeline", str(ETL_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_retries(monkeypatch, tmp_path):
    module = load_module()
    # prepare a small row generator
    rows = ({"name": f"u{i}", "value": i} for i in range(3))
    db = tmp_path / "retry.db"

    # monkeypatch sqlite3.Cursor.executemany to fail twice then succeed
    orig = sqlite3.Cursor.executemany
    state = {"counter": 0}

    def flaky(self, sql, seq):
        # fail first two calls
        if state["counter"] < 2:
            state["counter"] += 1
            raise sqlite3.OperationalError("simulated transient")
        return orig(self, sql, seq)

    monkeypatch.setattr(sqlite3.Cursor, "executemany", flaky)

    # run load and expect it to succeed despite transient failures
    total = module.load(rows, db_path=db, batch_size=1, progress_interval=0, create_index=False, fast=False, max_retries=5, retry_delay=0.01, logger=None)
    # verify rows in DB
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sample")
    c = cur.fetchone()[0]
    conn.close()
    assert c == total == 3

import subprocess
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEANING_SCRIPT = ROOT / "code" / "cleaning_script.py"
RAW_CSV = ROOT / "data" / "raw" / "sample.csv"


def test_clean_removes_empty_rows(tmp_path):
    # create CSV with empty rows
    csv = tmp_path / "test_empty.csv"
    csv.write_text("id,name,value\n1,Alice,10\n,,\n3,Bob,20\n")
    out = tmp_path / "out.csv"
    cmd = ["python3", str(CLEANING_SCRIPT), "--input", str(csv), "--output", str(out)]
    subprocess.check_call(cmd)
    # verify empty row was dropped
    df = pd.read_csv(out)
    assert len(df) == 2
    assert list(df["id"]) == [1.0, 3.0]


def test_clean_strips_whitespace(tmp_path):
    csv = tmp_path / "test_spaces.csv"
    csv.write_text("id,name\n1, Alice \n2, Bob \n")
    out = tmp_path / "out.csv"
    cmd = ["python3", str(CLEANING_SCRIPT), "--input", str(csv), "--output", str(out)]
    subprocess.check_call(cmd)
    df = pd.read_csv(out)
    assert df["name"].iloc[0] == "Alice"  # no leading/trailing spaces


def test_clean_handles_missing_file():
    cmd = ["python3", str(CLEANING_SCRIPT), "--input", "/nonexistent/file.csv"]
    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode != 0


def test_clean_with_sample_csv():
    if not RAW_CSV.exists():
        return  # skip if no sample data
    out = ROOT / "data" / "cleaned" / "cleaned_test.csv"
    cmd = ["python3", str(CLEANING_SCRIPT), "--input", str(RAW_CSV), "--output", str(out), "--profile"]
    subprocess.check_call(cmd)
    assert out.exists()
    df = pd.read_csv(out)
    assert len(df) > 0

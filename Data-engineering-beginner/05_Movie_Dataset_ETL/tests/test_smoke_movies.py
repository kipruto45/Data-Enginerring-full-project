import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "code" / "movie_etl.py"
RAW_LARGE = ROOT / "data" / "raw" / "movies_large.csv"
RESULT = ROOT / "results" / "movies_summary.csv"


def test_movies_large_csv_exists():
    assert RAW_LARGE.exists()
    assert sum(1 for _ in RAW_LARGE.open()) == 100001


def test_top_genres_and_summary_write(tmp_path):
    # import module and run top_genres on the large csv
    spec = importlib.util.spec_from_file_location("movie_etl", str(MODULE))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    top = m.top_genres(str(RAW_LARGE), top_n=5)
    assert isinstance(top, list)
    assert len(top) > 0

    # write a summary to results and verify
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    with RESULT.open("w", newline="", encoding="utf-8") as f:
        f.write("genre,count\n")
        for g, c in top:
            f.write(f"{g},{c}\n")
    assert RESULT.exists()
    with RESULT.open() as f:
        assert f.readline().strip() == "genre,count"

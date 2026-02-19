"""Generate synthetic weather observation CSV data

Usage:
    python generate_weather_data.py --rows 100000 --out ../data/raw/weather_observations_large.csv
"""

import csv
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "raw" / "weather_observations_large.csv"

STATIONS = ["StationA","StationB","StationC","StationD","StationE"]
CONDITIONS = ["Sunny","Cloudy","Rain","Snow","Windy","Fog"]


def generate(out_path, rows=100000):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2021,1,1)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["obs_id","station","date","temp_c","condition","humidity"])
        for i in range(rows):
            date = start + timedelta(minutes=random.randint(0, 525600))  # up to a year in minutes
            station = random.choice(STATIONS)
            temp = round(random.uniform(-20.0,40.0),1)
            condition = random.choice(CONDITIONS)
            humidity = random.randint(10,100)
            writer.writerow([i+1, station, date.strftime("%Y-%m-%d %H:%M:%S"), temp, condition, humidity])
    print(f"Wrote {rows} rows to {out}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--rows', type=int, default=100000)
    p.add_argument('--out', type=str, default=str(DEFAULT_OUT))
    args = p.parse_args()
    generate(args.out, args.rows)

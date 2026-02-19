"""Weather data ETL starter

This script demonstrates fetching from an API (placeholder) and storing a summary CSV.
Replace the `fetch_weather` function with real API calls and add your API key.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "weather_summary.csv"


def fetch_weather(location):
    # Placeholder: return a dict with sample fields
    return {"location": location, "temp_c": 20.5, "condition": "Sunny"}


def save_summary(rows):
    with open(RESULT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    locations = ["Nairobi", "London", "New York"]
    rows = [fetch_weather(loc) for loc in locations]
    save_summary(rows)
    print(f"Wrote weather summary to {RESULT}")

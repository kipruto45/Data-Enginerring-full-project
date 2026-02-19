# 04_Weather_Data_API

Operational notes for the starter weather ETL script.

## Run Script

```bash
python code/weather_etl.py
```

## Current Behavior

- Uses hardcoded locations (`Nairobi`, `London`, `New York`)
- Calls placeholder `fetch_weather()` logic
- Writes output CSV to `results/weather_summary.csv`

## Recommended Next Improvements

- Externalize locations via CLI arguments
- Add real HTTP API integration
- Add logging, retries, and tests

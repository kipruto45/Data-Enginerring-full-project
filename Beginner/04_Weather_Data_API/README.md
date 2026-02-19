# 04_Weather_Data_API

Starter weather ETL project that writes a summary CSV from placeholder weather records.

## What This Project Demonstrates

- Basic ETL structure in a single Python script
- Placeholder API extraction function (`fetch_weather`)
- CSV output generation to `results/weather_summary.csv`

## Run

```bash
python code/weather_etl.py
```

## Output

- `results/weather_summary.csv`

## Extending This Project

1. Replace `fetch_weather()` with real API calls (for example NOAA or OpenWeather).
2. Add retries and timeout handling.
3. Add input parameterization for locations.
4. Add tests and schema validation.

## Note

For a full pipeline version with synthetic data generation, batching, and tests, use `Data-engineering-beginner/04_Weather_Data_API`.

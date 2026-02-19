# 04_IoT_Sensor_Data_Collection

IoT sensor pipeline for generating time-series readings, detecting anomalies, and writing hourly aggregates to SQLite.

## What You Learn

- Simulated high-frequency sensor data generation
- Statistical anomaly detection using standard deviation thresholds
- Time-bucketed aggregation for operational reporting

## Quick Start

```bash
pip install -r requirements.txt
python code/iot_pipeline.py --generate --samples 10000
python code/iot_pipeline.py --input data/raw/sensor_data.csv --db results/iot_data.db
```

## Verify

```bash
sqlite3 results/iot_data.db "SELECT COUNT(*) FROM sensor_readings;"
```

See `docs/README.md` for schema and extension guidance.

# 04_IoT_Sensor_Data_Collection

**Real-time Time-Series Data from IoT Sensors**

Demonstrates:
- High-frequency data ingestion
- Sensor anomaly detection
- Time-bucketed aggregations
- Windowing and rolling calculations
- Streaming-like patterns in batch

## Quick Start

1. Generate simulated sensor data:
```bash
python code/iot_pipeline.py --generate --samples 10000
```

2. Load and process:
```bash
python code/iot_pipeline.py --input data/raw/sensor_data.csv --db results/iot_data.db
```

3. Query aggregates:
```bash
sqlite3 results/iot_data.db
SELECT sensor_id, hour, avg_value, anomaly_count 
FROM sensor_aggregates_hourly 
WHERE anomaly_count > 0;
```

## Features

**Sensor Simulation:**
- 4 sensor types (temperature, humidity, pressure)
- Realistic value ranges with Gaussian noise
- ~5% anomalies injected

**Anomaly Detection:**
- Statistical method (standard deviation threshold)
- Configurable sensitivity
- Flags anomalies for investigation

**Time-Bucketed Aggregates:**
- Hourly rollups (min, max, avg, count)
- Anomaly counts per hour
- Efficient storage and querying

**Schema:**
- `sensor_readings`: Raw measurements with anomaly flags
- `sensor_aggregates_hourly`: Pre-computed hourly stats

## Use Cases

- Monitoring equipment health
- Early warning for failures
- Trend analysis and forecasting
- SLA tracking (uptime, reliability)
- Real-time dashboards

## CLI Options

- `--input`: Input CSV path
- `--db`: Output DB path
- `--generate`: Generate sample data
- `--samples`: Number of sensor readings
- `--anomaly-threshold`: Anomaly detection sensitivity (std devs)
- `--log-level`: Logging level

## Scaling Tips

- Use time-series DB (InfluxDB, TimescaleDB) for production
- Implement streaming processing (Kafka, Spark Streaming)
- Partition data by time for efficient queries
- Use compression for long-term storage

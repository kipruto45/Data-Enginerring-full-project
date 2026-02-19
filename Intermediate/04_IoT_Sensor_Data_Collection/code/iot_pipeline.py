"""IoT Sensor Data Collection and Processing

Demonstrates:
- High-frequency time-series data ingestion
- Window-based aggregations
- Real-time streaming-like processing
- Sensor anomaly detection
- Time-bucketing for efficient storage
"""

import sqlite3
import csv
import logging
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "raw" / "sensor_data.csv"
DEFAULT_DB = ROOT / "results" / "iot_data.db"


def setup_logger(level=logging.INFO):
    logger = logging.getLogger("iot_etl")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def parse_args():
    p = argparse.ArgumentParser(description="IoT Sensor Data ETL")
    p.add_argument("--input", default=str(DEFAULT_DATA), help="Input CSV path")
    p.add_argument("--db", default=str(DEFAULT_DB), help="Output DB path")
    p.add_argument("--generate", action="store_true", help="Generate sample data")
    p.add_argument("--samples", type=int, default=10000, help="Number of samples")
    p.add_argument("--anomaly-threshold", type=float, default=2.0, help="Anomaly detection threshold (std devs)")
    p.add_argument("--log-level", default="INFO", help="Logging level")
    return p.parse_args()


def generate_sensor_data(csv_path, num_samples=10000, logger=None):
    """Generate simulated IoT sensor readings"""
    sensors = ["temp_sensor_1", "temp_sensor_2", "humidity_sensor_1", "pressure_sensor_1"]
    base_time = datetime.now() - timedelta(hours=24)
    
    rows = []
    for i in range(num_samples):
        sensor = random.choice(sensors)
        timestamp = base_time + timedelta(seconds=i * 8)  # ~8 second intervals (1 sample every 8s per sensor)
        
        # Generate realistic sensor data with occasional spikes
        if random.random() > 0.95:  # 5% anomalies
            value = random.uniform(100, 150)  # Anomaly
        else:
            if "temp" in sensor:
                value = 20 + random.gauss(0, 2)  # Mean 20°C, std 2°C
            elif "humidity" in sensor:
                value = 50 + random.gauss(0, 5)  # Mean 50%, std 5%
            else:
                value = 1013 + random.gauss(0, 10)  # Mean 1013 hPa, std 10 hPa
        
        rows.append({
            "sensor_id": sensor,
            "timestamp": timestamp.isoformat(),
            "value": round(value, 2),
            "unit": "C" if "temp" in sensor else ("%" if "humidity" in sensor else "hPa")
        })
    
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    if logger:
        logger.info(f"Generated {num_samples} sensor samples to {csv_path}")


def create_iot_schema(db_path, logger=None):
    """Create IoT data schema"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Raw sensor readings
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            timestamp TEXT,
            value REAL,
            unit TEXT,
            is_anomaly INTEGER DEFAULT 0,
            ingested_at TEXT
        )
    """)
    
    # Time-bucketed aggregations (hourly)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_aggregates_hourly (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            hour TEXT,
            min_value REAL,
            max_value REAL,
            avg_value REAL,
            count INTEGER,
            anomaly_count INTEGER
        )
    """)
    
    conn.commit()
    conn.close()
    if logger:
        logger.info("Created IoT schema: sensor_readings, sensor_aggregates_hourly")


def detect_anomalies(readings, threshold=2.0, logger=None):
    """Detect anomalies using simple statistical method"""
    if len(readings) < 3:
        return readings
    
    values = [r["value"] for r in readings]
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance ** 0.5
    
    anomalies = 0
    for r in readings:
        if abs(r["value"] - mean) > threshold * std_dev:
            r["is_anomaly"] = 1
            anomalies += 1
    
    if logger and anomalies > 0:
        logger.info(f"Detected {anomalies} anomalies (threshold: {threshold} std devs)")
    
    return readings


def load_iot_data(csv_path, db_path, anomaly_threshold=2.0, logger=None):
    """Load and process IoT data"""
    create_iot_schema(db_path, logger)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    readings = []
    row_count = 0
    
    # Read CSV
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append({
                "sensor_id": row["sensor_id"],
                "timestamp": row["timestamp"],
                "value": float(row["value"]),
                "unit": row["unit"],
                "is_anomaly": 0
            })
            row_count += 1
    
    if logger:
        logger.info(f"Loaded {row_count} readings from CSV")
    
    # Detect anomalies
    readings = detect_anomalies(readings, threshold=anomaly_threshold, logger=logger)
    
    # Insert readings
    now = datetime.now().isoformat()
    for r in readings:
        cur.execute("""
            INSERT INTO sensor_readings (sensor_id, timestamp, value, unit, is_anomaly, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["sensor_id"], r["timestamp"], r["value"], r["unit"], r["is_anomaly"], now))
    
    conn.commit()
    
    # Create hourly aggregates
    cur.execute("""
        INSERT INTO sensor_aggregates_hourly (sensor_id, hour, min_value, max_value, avg_value, count, anomaly_count)
        SELECT 
            sensor_id,
            DATE(timestamp) || 'T' || SUBSTR(timestamp, 12, 2) || ':00:00' as hour,
            MIN(value),
            MAX(value),
            AVG(value),
            COUNT(*),
            SUM(is_anomaly)
        FROM sensor_readings
        GROUP BY sensor_id, hour
    """)
    
    conn.commit()
    
    total_readings = cur.execute("SELECT COUNT(*) FROM sensor_readings").fetchone()[0]
    total_anomalies = cur.execute("SELECT SUM(is_anomaly) FROM sensor_readings").fetchone()[0] or 0
    
    conn.close()
    
    if logger:
        logger.info(f"IoT data processed: {total_readings} readings, {total_anomalies} anomalies")
    
    return row_count


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logger(getattr(logging, args.log_level.upper(), logging.INFO))
    
    csv_path = Path(args.input)
    
    if args.generate:
        generate_sensor_data(csv_path, num_samples=args.samples, logger=logger)
    
    if csv_path.exists():
        load_iot_data(csv_path, args.db, anomaly_threshold=args.anomaly_threshold, logger=logger)
        logger.info(f"IoT ETL complete: {args.db}")
    else:
        logger.error(f"Input file not found: {csv_path}")
        raise SystemExit(1)

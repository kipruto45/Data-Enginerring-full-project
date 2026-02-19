# 02_Airflow_ETL_Pipeline

**Workflow Orchestration with Apache Airflow**

Demonstrates task scheduling, dependencies, and monitoring:
- DAGs (Directed Acyclic Graphs) for workflow definition
- Task dependencies and parallel execution
- Error handling and retries
- Monitoring and alerting
- XCom for inter-task communication

## Setup

1. Install Airflow:
```bash
pip install apache-airflow
```

2. Initialize Airflow DB:
```bash
airflow db init
```

3. Place DAG:
```bash
cp dags/main_dag.py ~/airflow/dags/
```

4. Start Airflow scheduler and webserver:
```bash
airflow scheduler &
airflow webserver
```

5. Open http://localhost:8080 and enable the DAG

## DAG Structure

**Tasks:**
- `extract`: Fetch data from source (simulated, 10,000 rows)
- `transform`: Apply transformations
- `validate`: Data quality checks
- `load`: Load to warehouse
- `notify`: Send completion notification

**Dependencies:** extract → transform → validate → load → notify

**Schedule:** Daily (@daily)

**Retries:** 2 attempts with 5-minute backoff

## Features

- Task monitoring in web UI
- Automatic retries on failure
- XCom for passing data between tasks
- Logs accessible via UI
- Easy task dependency visualization

## Production Considerations

- Use robust sensors (external task sensors, HTTP sensors)
- Implement SLA monitoring
- Set up alerting for failures
- Use connections for secrets management
- Scale with distributed executors

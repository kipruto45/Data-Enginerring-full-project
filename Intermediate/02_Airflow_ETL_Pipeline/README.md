# 02_Airflow_ETL_Pipeline

Airflow orchestration example for a staged ETL flow (`extract -> transform -> validate -> load -> notify`).

## What You Learn

- DAG structure and task dependencies
- Retry configuration and scheduling
- XCom-style task communication
- Local dry-run strategy without full Airflow install

## Quick Start

```bash
pip install -r requirements.txt
python code/dry_run.py --tasks extract,transform,validate,load,notify --verbose
```

For full Airflow setup and DAG deployment, see `docs/README.md`.

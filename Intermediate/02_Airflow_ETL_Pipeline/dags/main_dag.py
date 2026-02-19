"""Apache Airflow DAG for ETL Pipeline

This DAG demonstrates task orchestration:
- Task dependencies (A -> B -> C)
- Parallel tasks (D, E run together)
- Error handling and retries
- Task monitoring and logging
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

default_args = {
    'owner': 'data-eng',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 1, 1),
}

dag = DAG(
    'etl_pipeline_dag',
    default_args=default_args,
    description='ETL pipeline with task dependencies',
    schedule_interval='@daily',
    catchup=False,
)

logger = logging.getLogger(__name__)


def extract_data(**context):
    """Extract data from source"""
    logger.info("Extracting data from source...")
    # Simulate data extraction
    context['task_instance'].xcom_push(key='extracted_rows', value=10000)
    logger.info("Extraction complete: 10000 rows")


def transform_data(**context):
    """Transform extracted data"""
    ti = context['task_instance']
    rows = ti.xcom_pull(task_ids='extract', key='extracted_rows')
    logger.info(f"Transforming {rows} rows...")
    # Simulate transformation
    ti.xcom_push(key='transformed_rows', value=rows)
    logger.info(f"Transformation complete")


def validate_data(**context):
    """Validate transformed data"""
    ti = context['task_instance']
    rows = ti.xcom_pull(task_ids='transform', key='transformed_rows')
    logger.info(f"Validating {rows} rows...")
    if rows > 0:
        logger.info("Validation passed")
    else:
        raise ValueError("No data to validate")


def load_to_warehouse(**context):
    """Load data into warehouse"""
    ti = context['task_instance']
    rows = ti.xcom_pull(task_ids='transform', key='transformed_rows')
    logger.info(f"Loading {rows} rows to warehouse...")
    logger.info("Load complete")


def send_notification(**context):
    """Send notification on success"""
    logger.info("ETL pipeline completed successfully")


# Define tasks
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate',
    python_callable=validate_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_to_warehouse,
    dag=dag,
)

notify_task = PythonOperator(
    task_id='notify',
    python_callable=send_notification,
    dag=dag,
)

# Set dependencies: extract -> transform -> validate -> load -> notify
extract_task >> transform_task >> validate_task >> load_task >> notify_task

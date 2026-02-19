import importlib
import types
import sys
import os

# Add project root to sys.path so dags module can be imported
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Inject minimal airflow stubs
airflow_stub = types.ModuleType("airflow")

class StubDAG:
    def __init__(self, *args, **kwargs):
        self.dag_id = kwargs.get("dag_id", args[0] if args else "stub_dag")

class StubPythonOperator:
    def __init__(self, task_id=None, python_callable=None, dag=None, **kwargs):
        self.task_id = task_id
        self.python_callable = python_callable
        self.dag = dag

    def __rshift__(self, other):
        return other

    def __lshift__(self, other):
        return other

airflow_stub.DAG = StubDAG

modops = types.ModuleType('airflow.operators')
modpy = types.ModuleType('airflow.operators.python')
modpy.PythonOperator = StubPythonOperator
modops.python = modpy

sys.modules['airflow'] = airflow_stub
sys.modules['airflow.operators'] = modops
sys.modules['airflow.operators.python'] = modpy

# Import DAG module
mod = importlib.import_module('dags.main_dag')

# Access callables
extract = getattr(mod, 'extract_data')
transform = getattr(mod, 'transform_data')
validate = getattr(mod, 'validate_data')
load = getattr(mod, 'load_to_warehouse')

# Simple TaskInstance stub
class TI:
    def __init__(self):
        self._x = {}
    def xcom_push(self, key, value):
        self._x[key] = value
    def xcom_pull(self, task_ids=None, key=None):
        return self._x.get(key)


def test_extract_transform_validate_load_success():
    ti1 = TI()
    extract(task_instance=ti1)
    assert ti1.xcom_pull(key='extracted_rows') == 10000

    ti2 = TI()
    # simulate extract xcom
    ti2.xcom_push('extracted_rows', 10000)
    transform(task_instance=ti2)
    assert ti2.xcom_pull(key='transformed_rows') == 10000

    ti3 = TI()
    ti3.xcom_push('transformed_rows', 10000)
    validate(task_instance=ti3)  # should not raise

    ti4 = TI()
    ti4.xcom_push('transformed_rows', 10000)
    load(task_instance=ti4)  # should not raise


def test_validate_fails_on_zero_rows():
    ti = TI()
    ti.xcom_push('transformed_rows', 0)
    try:
        validate(task_instance=ti)
    except ValueError as e:
        assert 'No data to validate' in str(e)
    else:
        assert False, "validate should raise ValueError when rows == 0"

"""Dry-run utility for ETL DAG without Airflow installed

Usage:
  python3 code/dry_run.py --tasks extract,transform,validate,load,notify
"""
import sys
import argparse
import importlib
import types
import time
import logging

logger = logging.getLogger("dry_run")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def inject_stub_airflow():
    """Inject minimal airflow stubs so `dags.main_dag` can be imported."""
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
            # Support >> operator for task dependencies
            return other

        def __lshift__(self, other):
            # Support << operator for task dependencies
            return other

    # Add DAG to the airflow module
    airflow_stub.DAG = StubDAG

    operators_mod = types.ModuleType("airflow.operators")
    python_mod = types.ModuleType("airflow.operators.python")
    python_mod.PythonOperator = StubPythonOperator
    operators_mod.python = python_mod

    sys.modules["airflow"] = airflow_stub
    sys.modules["airflow.operators"] = operators_mod
    sys.modules["airflow.operators.python"] = python_mod


class DummyTI:
    def __init__(self):
        self._xcom = {}

    def xcom_push(self, key, value):
        self._xcom[key] = value

    def xcom_pull(self, task_ids=None, key=None):
        return self._xcom.get(key)


def discover_tasks(module):
    tasks = {}
    for name, obj in vars(module).items():
        if hasattr(obj, "python_callable") and getattr(obj, "task_id", None):
            tasks[obj.task_id] = obj.python_callable
    return tasks


def run_tasks(tasks, order):
    metrics = []
    xcom_store = {}

    for t in order:
        func = tasks.get(t)
        if not func:
            logger.warning("Task not found: %s", t)
            continue
        ti = DummyTI()

        # Populate ti with previous xcoms (simple behavior)
        for k, v in xcom_store.items():
            ti._xcom[k] = v

        logger.info("Running %s...", t)
        start = time.perf_counter()
        try:
            func(**{"task_instance": ti})
            elapsed = time.perf_counter() - start
            # capture pushes
            xcom_store.update(ti._xcom)
            metrics.append((t, "ok", elapsed))
            logger.info("%s finished in %.6fs", t, elapsed)
        except Exception as e:
            elapsed = time.perf_counter() - start
            metrics.append((t, "error", elapsed, str(e)))
            logger.exception("%s failed: %s", t, e)
            break

    return metrics


def main():
    p = argparse.ArgumentParser(description="Dry-run ETL DAG without Airflow")
    p.add_argument("--tasks", default="extract,transform,validate,load,notify", help="Comma-separated task order to run")
    p.add_argument("--module", default="dags.main_dag", help="DAG module to import")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    inject_stub_airflow()

    # Add project root to sys.path so dags module can be imported
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

    try:
        mod = importlib.import_module(args.module)
    except Exception:
        logger.exception("Failed to import DAG module %s", args.module)
        sys.exit(2)

    tasks = discover_tasks(mod)
    order = [t.strip() for t in args.tasks.split(",") if t.strip()]

    logger.info("Discovered tasks: %s", list(tasks.keys()))
    metrics = run_tasks(tasks, order)

    logger.info("Dry-run complete. Metrics:")
    for m in metrics:
        logger.info(m)


if __name__ == "__main__":
    main()

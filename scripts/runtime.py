"""Serializa el acceso a DuckDB y propaga el código de salida de dbt."""
import fcntl
import subprocess
from contextlib import contextmanager


@contextmanager
def warehouse_lock():
    with open("/data/warehouse.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def run_dbt(arguments):
    with warehouse_lock():
        print("INICIO dbt", arguments, flush=True)
        subprocess.run(["/opt/dbt/bin/dbt", *arguments, "--project-dir", "/workspace/dbt",
                        "--profiles-dir", "/workspace/dbt"], check=True)
        print("FIN dbt", arguments, flush=True)

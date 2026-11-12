"""Diagnóstico operativo de lectura, escritura y persistencia dentro del contenedor."""
import os
import pwd
from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb


def check_environment():
    assert os.getuid() != 0 and os.getgid() == 0, "Se requiere un usuario no root con GID 0"
    print(f"Usuario resuelto: {pwd.getpwuid(os.getuid()).pw_name}, UID={os.getuid()}, GID={os.getgid()}")
    for folder in ("dbt", "scripts", "airflow/dags", "data"):
        for path in (Path("/workspace") / folder).rglob("*"):
            if path.is_file():
                with path.open("rb") as source:
                    source.read(1)
    assert not os.access("/workspace", os.W_OK), "El montaje del repositorio debe ser de solo lectura"
    print("OK: proyecto legible y montaje de solo lectura")
    for folder in ("/data", "/state", "/state/logs", "/state/dbt/target", "/state/dbt/logs"):
        Path(folder).mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(prefix="comprobacion-", dir=folder) as temporary:
            probe = Path(temporary) / "escritura.txt"
            probe.write_text("correcto", encoding="utf-8")
            assert probe.read_text(encoding="utf-8") == "correcto"
        print(f"OK: escritura y reapertura en {folder}")
    with TemporaryDirectory(prefix="comprobacion-duckdb-", dir="/data") as temporary:
        database = str(Path(temporary) / "prueba.duckdb")
        with duckdb.connect(database) as connection:
            connection.execute("create table comprobacion as select 42 as valor")
        with duckdb.connect(database) as connection:
            assert connection.execute("select valor from comprobacion").fetchone() == (42,)
    database = Path("/data/ventas.duckdb")
    if database.exists():
        with duckdb.connect(str(database)) as connection:
            connection.execute("select 1").fetchone()
        print("OK: reapertura de ventas.duckdb existente")
    print("OK: creación, escritura y reapertura de DuckDB. Archivos temporales eliminados")

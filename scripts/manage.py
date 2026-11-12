"""Herramientas operativas que conservan el proyecto académico."""
import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import duckdb
from runtime import run_dbt, warehouse_lock

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["scenario", "dbt", "query", "artifacts", "check"])
parser.add_argument("arguments", nargs=argparse.REMAINDER)
args = parser.parse_args()
if args.action == "check":
    from check_environment import check_environment
    with warehouse_lock():
        check_environment()
elif args.action == "dbt":
    run_dbt(args.arguments)
elif args.action == "artifacts":
    for name in ("sources.json", "run_results.json"):
        path = Path("/state/dbt/target") / name
        print(name)
        print(path.read_text() if path.exists() else "Todavía no existe")
else:
    with warehouse_lock(), duckdb.connect("/data/ventas.duckdb") as con:
        con.execute("SET TimeZone='UTC'")
        if args.action == "scenario":
            hours = {"actualizada": 2, "advertencia": 18, "desactualizada": 30}
            if len(args.arguments) != 1 or args.arguments[0] not in hours:
                parser.error("scenario requiere actualizada, advertencia o desactualizada")
            loaded = datetime.now(timezone.utc) - timedelta(hours=hours[args.arguments[0]])
            with open("/workspace/data/ventas.csv", newline="") as file:
                rows = [(int(r["id_venta"]), r["fecha_venta"], int(r["cantidad"]),
                         Decimal(r["precio_unitario"]), loaded) for r in csv.DictReader(file)]
            con.execute("BEGIN")
            con.execute("CREATE SCHEMA IF NOT EXISTS raw")
            con.execute("CREATE TABLE IF NOT EXISTS raw.ventas (id_venta INTEGER PRIMARY KEY, fecha_venta DATE NOT NULL, cantidad INTEGER NOT NULL, precio_unitario DECIMAL(12,2) NOT NULL, _loaded_at TIMESTAMPTZ NOT NULL)")
            con.execute("DELETE FROM raw.ventas")
            con.executemany("INSERT INTO raw.ventas VALUES (?, ?, ?, ?, ?)", rows)
            con.execute("COMMIT")
            print(json.dumps({"scenario": args.arguments[0], "rows": len(rows), "max_loaded_at": loaded.isoformat()}))
        else:
            sql = " ".join(args.arguments)
            if not sql:
                parser.error("query requiere una consulta SQL")
            result = con.execute(sql)
            print([c[0] for c in result.description])
            for row in result.fetchall():
                print(row)

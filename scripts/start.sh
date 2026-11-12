#!/usr/bin/env bash
set -euo pipefail
airflow db migrate
python /workspace/scripts/admin.py
airflow webserver &
web_pid=$!
airflow scheduler &
scheduler_pid=$!
trap 'kill "$web_pid" "$scheduler_pid" 2>/dev/null || true; wait' TERM INT EXIT
wait -n "$web_pid" "$scheduler_pid"
exit 1

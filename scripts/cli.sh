#!/usr/bin/env bash
set -euo pipefail
exec /opt/dbt/bin/python /workspace/scripts/manage.py "$@"

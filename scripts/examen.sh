#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# El anfitrión solo ejecuta Bash y Docker. Python y dbt viven en la imagen.
bash scripts/preparar.sh
docker compose run --rm cli "$@"

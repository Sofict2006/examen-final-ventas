#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# No se ejecuta ni se sobrescribe un .env existente.
if [ -e .env ]; then
    exit 0
fi
examen_uid=$(id -u)
if [ "$examen_uid" = 0 ]; then
    printf '%s\n' 'Ejecute este script con su usuario habitual, sin sudo.' >&2
    exit 1
fi
(umask 077; set -C; printf 'AIRFLOW_UID=%s\n' "$examen_uid" > .env)
printf '%s\n' "Creado .env local con AIRFLOW_UID=$examen_uid."

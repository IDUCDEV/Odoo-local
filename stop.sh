#!/usr/bin/env bash
# Detiene Odoo. Los datos quedan guardados en ./data (no se borra nada).
set -e
cd "$(dirname "$0")"

docker compose down
echo "Odoo detenido. Tus datos siguen en ./data"

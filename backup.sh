#!/usr/bin/env bash
# Crea un respaldo de la base de datos en backups/odoo-FECHA.sql.gz
set -e
cd "$(dirname "$0")"

mkdir -p backups
STAMP=$(date +%Y%m%d-%H%M%S)
FILE="backups/odoo-$STAMP.sql.gz"

docker compose exec -T db pg_dump -U odoo odoo | gzip > "$FILE"

echo "Respaldo creado: $FILE ($(du -h "$FILE" | cut -f1))"

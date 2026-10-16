#!/usr/bin/env bash
# Restaura un respaldo creado con backup.sh. REEMPLAZA la base de datos actual.
# Uso:  ./restore.sh backups/odoo-20260101-120000.sql.gz
set -e
cd "$(dirname "$0")"

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Uso: ./restore.sh backups/odoo-YYYYMMDD-HHMMSS.sql.gz"
  echo ""
  echo "Respaldos disponibles:"
  ls -1 backups/ 2>/dev/null || echo "  (ninguno todavia)"
  exit 1
fi
if [ ! -f "$FILE" ]; then
  echo "No existe el archivo: $FILE"
  exit 1
fi

echo "ATENCION: esto REEMPLAZA la base de datos actual 'odoo' con: $FILE"
read -r -p "¿Continuar? (s/N): " CONF
if [ "$CONF" != "s" ] && [ "$CONF" != "S" ]; then
  echo "Cancelado."
  exit 1
fi

echo "-> Deteniendo Odoo..."
docker compose stop odoo

echo "-> Recreando base de datos..."
docker compose exec -T db psql -U odoo -d postgres -c "DROP DATABASE IF EXISTS odoo WITH (FORCE);"
docker compose exec -T db psql -U odoo -d postgres -c "CREATE DATABASE odoo OWNER odoo;"

echo "-> Importando respaldo..."
gunzip -c "$FILE" | docker compose exec -T db psql -q -U odoo -d odoo

echo "-> Levantando Odoo..."
docker compose start odoo

echo "Restauracion completada."

#!/usr/bin/env bash
# Levanta Odoo (web + base de datos) en segundo plano.
set -e
cd "$(dirname "$0")"

# Asegura que existan las carpetas de datos portables y que Odoo (uid 101
# dentro del contenedor) pueda escribir en el filestore, sin importar con
# que usuario estes en esta maquina.
mkdir -p data/db data/odoo
chmod -R 777 data/odoo 2>/dev/null || true

docker compose up -d

echo ""
echo "==================================================="
echo "  Odoo esta arrancando..."
echo "  Abre:  http://localhost:8069"
echo "  (la primera vez puede tardar 1-2 minutos)"
echo "==================================================="

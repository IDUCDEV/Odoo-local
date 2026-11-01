# Odoo local portable — IDUCDEV

Odoo Community en Docker, **portátil**: toda la base de datos y los archivos
viven dentro de esta carpeta. Copias la carpeta a otra máquina, ejecutas
`./start.sh` y tienes exactamente el mismo Odoo.

Pensado para un freelancer Flutter: clientes, cotizaciones, contratos y facturas.

## Módulos instalados

| App en Odoo | Módulo técnico | Para qué |
|---|---|---|
| Contactos | `contacts` | Clientes y proveedores |
| Ventas | `sale_management` | Cotizaciones / órdenes de venta |
| Facturación | `account` | Facturas y pagos |
| Contratos (OCA) | `contract` | Contratos recurrentes que generan facturas automáticamente |
| CRM *(por instalar)* | `crm` + `sale_crm` | Pipeline de oportunidades enlazado a las cotizaciones |

## Uso diario

```bash
./start.sh      # levanta Odoo -> http://localhost:8069
./stop.sh       # detiene Odoo (los datos quedan en ./data)
./backup.sh     # crea un respaldo en ./backups/odoo-FECHA.sql.gz
./restore.sh backups/odoo-FECHA.sql.gz   # restaura un respaldo
```

La primera vez que abras http://localhost:8069 verás el login. Crea la base
`odoo` desde ahí o entra con la que ya existe. Para gestionar bases de datos:
http://localhost:8069/web/database/manager (contraseña maestra: `admin`,
definida en `odoo.conf`).

## Flujo de un cliente

**▶ [GUIA-CLIENTE.md](./GUIA-CLIENTE.md)** — playbook completo paso a paso:
desde el lead del formulario web hasta la factura cobrada, facturación por
hitos o con anticipos, contratos de mantenimiento recurrente, plantillas de
correo y condiciones, errores típicos y ficha imprimible. Pensado para
Odoo 19 Community en local facturando en **USD con IVA venezolano**.

Resumen de las 3 ideas:

1. **CRM → Cotización → Orden de venta → Factura → Cobro.** Instala la app
   CRM (`crm`; `sale_crm` va solo) y usa la localización de Venezuela
   (`l10n_ve`) poniendo el país en la compañía para tener IVA listo.
2. **Proyectos por hitos**: una orden de venta con una línea por fase y
   política "cantidades entregadas"; marcas la cantidad entregada de cada fase
   al terminarla y "Crear factura" solo factura lo entregado. Para el
   mantenimiento mensual usa la app Contratos (OCA `contract`).
3. **Community no tiene** firma online de cotizaciones, suscripciones ni
   Timesheets; lo demás (facturación, impuestos, anticipos, portal, Stripe)
   funciona igual.

## Llevar todo a otra máquina (nueva laptop)

1. **Instala Docker** (Docker Desktop o Docker Engine + el plugin `docker compose`).
2. **Copia esta carpeta completa** (incluida `data/`, que es lo importante).
   ```bash
   # ejemplo con rsync desde la máquina vieja
   rsync -av "mi setup odoo - IDUCDEV/" usuario@nueva-maquina:~/odoo/
   ```
3. **Arranca** en la máquina nueva:
   ```bash
   cd ~/odoo/"mi setup odoo - IDUCDEV"   # ajusta el nombre si lo cambiaste
   ./start.sh
   ```
4. Abre http://localhost:8069 — mismos clientes, cotizaciones, contratos y facturas.

> `start.sh` ya se encarga de crear las carpetas y ajustar los permisos del
> filestore, así que no hace falta configurar nada por el cambio de usuario/máquina.

## Estructura

```
├── docker-compose.yml   # Odoo + PostgreSQL (versiones en odoo:latest y postgres:15)
├── odoo.conf            # configuración de Odoo (rutas de addons, conexión BD)
├── extra-addons/
│   └── contract/        # repo OCA/contract (rama 19.0) con el módulo de contratos
├── data/                # ⚠️ TUS DATOS REALES (base de datos + filestore) NO se versiona
│   ├── db/              #   PostgreSQL completo
│   └── odoo/            #   filestore (PDFs, adjuntos, logos)
├── backups/             # respaldos .sql.gz (NO se versiona)
├── start.sh / stop.sh   # arranque y parada
├── backup.sh / restore.sh
├── README.md
└── GUIA-CLIENTE.md      # playbook de ventas: lead → cotización → factura
```

## Añadir más módulos de la OCA

La ruta de addons está fijada en `odoo.conf`. Para añadir otro repo:

```bash
git clone --depth 1 --branch 19.0 https://github.com/OCA/<repo> extra-addons/<repo>
rm -rf extra-addons/<repo>/.git     # opcional: dejar solo el código
```

Y añade la ruta al `addons_path` en `odoo.conf`, separada por coma:

```ini
addons_path = /mnt/extra-addons/contract,/mnt/extra-addons/<repo>
```

Reinicia con `./start.sh` (o `docker compose restart odoo`) y activa el módulo
desde Aplicaciones.

## Notas

- **Versión de Odoo**: usa la imagen `odoo:latest` (actualmente 19.0). Si una
  actualización rompe algo, fija la versión en `docker-compose.yml`
  (por ejemplo `image: odoo:19.0`) y reinicia.
- **Módulo de contratos**: si `contract` no carga, comprueba que la rama del repo
  OCA coincide con la versión mayor de Odoo (rama 19.0 para Odoo 19).
- **Contraseña maestra**: cambia `admin_passwd` en `odoo.conf` si expones el
  puerto fuera de tu equipo.
- **Bases de datos de prueba con demo**: desde el gestor de bases de datos puedes
  crear otra base (ej. `odoo-demo`) e instalar apps con datos de demostración para
  aprender sin ensuciar tu base real.
- **Setup antiguo**: la carpeta `~/odoo-docker` y sus volúmenes
  (`odoo-docker_pgdata`, `odoo-docker_odoodata`) se dejaron intactos. Cuando ya no
  los necesites:
  ```bash
  docker volume rm odoo-docker_pgdata odoo-docker_odoodata
  rm -rf ~/odoo-docker
  ```

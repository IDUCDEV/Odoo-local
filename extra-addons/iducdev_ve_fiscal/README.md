# Venezuela - Datos fiscales SENIAT (`iducdev_ve_fiscal`)

Módulo para **Odoo 19 Community** que registra en las facturas los datos que
exige la **Providencia Administrativa SNAT/2026/00093** del SENIAT, publicada
en la **Gaceta Oficial N° 43.484 del 21 de octubre de 2026** y vigente a los
**180 días continuos** de su publicación (**19 de abril de 2027**).

> El módulo **no emite** documentos fiscales. La emisión se hace por el portal
> del SENIAT, una imprenta digital autorizada o formatos de contingencia.
> Odoo registra el resultado y sigue siendo el sistema de gestión comercial.

## Qué añade

| Requisito | Norma | Implementación |
|---|---|---|
| Número de control (2 dígitos + hasta 8 secuenciales) | art. 8.3, 9.1 | Campo `x_control_number` con validación de formato y unicidad por compañía |
| Número de factura del medio autorizado | art. 9 | Campo `x_fiscal_number` |
| Fecha **y hora** de emisión | art. 8.5 | Campo `x_fiscal_datetime` (Odoo solo guarda la fecha) |
| Medio de emisión | art. 4 | Campo `x_fiscal_medium` |
| Estado del documento | art. 7 | Campo `x_fiscal_state` + recordatorio automático al día siguiente en contingencia |
| Marca `(E)` en líneas exentas o no gravadas | art. 8.7 | Reporte de factura |
| Tipo de cambio y total en bolívares | art. 8.12 | Campos `x_seniat_rate`, `x_ve_amount_total`, `x_ve_rate_used` + reporte |
| Frase de emisión conforme a la Providencia | art. 19 | Reporte de factura |
| Etiqueta "RIF" en lugar de "Tax ID" | art. 8.4 | `res.country` de Venezuela |
| Aviso si el cliente es extranjero y lleva IVA | art. 8.7 | Campo calculado `x_ve_tax_warning` (no bloqueante) |

## Instalación

1. El `odoo.conf` de este repositorio ya incluye `/mnt/extra-addons` en
   `addons_path`, y el `docker-compose.yml` monta `./extra-addons` en esa ruta.
2. Reiniciar Odoo:

   ```bash
   ./start.sh
   ```

3. Aplicaciones → **Actualizar lista de aplicaciones** → buscar
   "Venezuela - Datos fiscales SENIAT" → **Instalar**.

## Uso

1. Crear la factura en Odoo y dejarla en **borrador**.
2. Emitirla por el medio autorizado (portal del SENIAT, imprenta digital o
   talonario de contingencia).
3. En la factura, pestaña **Otra información → SENIAT (Venezuela)**, registrar:
   - Medio de emisión
   - N° Factura Fiscal
   - N° de Control
   - Fecha y hora de emisión fiscal
   - Tipo de cambio aplicado (si la factura está en divisa)
4. **Validar** la factura.
5. Adjuntar el PDF del SENIAT al chatter y enviar al cliente.

## Exigencia de los datos

Por defecto **no se bloquea** la validación, para poder seguir trabajando hasta
la entrada en vigencia. Cuando empiece a facturar por el portal del SENIAT,
active la casilla en **Ajustes → Contabilidad → "Exigir datos fiscales SENIAT
al validar"**.

A partir de ese momento, validar una factura de cliente sin número de control
ni fecha/hora fiscal lanza un error.

## Cliente extranjero (exportación)

Si el cliente está domiciliado fuera de Venezuela y el servicio se consume
fuera, la factura va con el impuesto `Exento (exportación)` (0 %). En ese caso:

- La línea sale marcada con **(E)** en el PDF (art. 8.7).
- El bloque de **tipo de cambio + total en bolívares** aparece igual, porque la
  factura está en divisa (art. 8.12).
- Si te olvidas y dejas IVA en alguna línea, la pestaña **SENIAT (Venezuela)**
  muestra un **aviso rojo**. No bloquea la validación: es solo un recordatorio
  (un cliente extranjero con establecimiento en Venezuela sí puede causar IVA).

## Limitaciones conocidas

- No hay integración automática con el portal del SENIAT ni con la API de una
  imprenta digital: el número se copia a mano.
- El PDF de Odoo es una **copia comercial**. El documento fiscal válido es el
  que emite el SENIAT.
- La marca "sin derecho a crédito fiscal" de las **copias** de documentos de
  contingencia (art. 11.3) no se distingue automáticamente: si imprime una
  copia, hágalo desde el talonario autorizado.
- El tipo de cambio se congela al guardar la factura. Si corrige el tipo de
  cambio después, vuelva a guardar la fecha de la factura para recalcular.

## Licencia

LGPL-3.

# Cumplimiento SENIAT — Providencia SNAT/2026/00093

Guía operativa para cumplir en este setup de Odoo 19 Community la
**Providencia Administrativa SNAT/2026/00093**, publicada en la **Gaceta
Oficial N° 43.484 del 21 de octubre de 2026**.

- **Entrada en vigencia:** 180 días continuos desde la publicación →
  **19 de abril de 2027**.
- **Documento fuente:** [`gaceta-43.484.pdf`](./gaceta-43.484.pdf) (escaneado,
  sin capa de texto).
- **Estrategia elegida:** *Opción A* — el documento fiscal lo emite el
  **portal web / app del SENIAT** (gratuito) y Odoo actúa como sistema de
  gestión comercial, registrando los datos con el módulo
  `iducdev_ve_fiscal`.

> ⚠️ Este documento resume la Providencia para uso operativo. **No sustituye
> la asesoría de tu contador ni del abogado tributarista**: confirma con ellos
> las alícuotas, los plazos y los trámites antes de facturar.

---

## 1. Qué exige la Providencia (resumen operativo)

| # | Requisito | Artículo | Cómo se cumple en este setup |
|---|---|---|---|
| 1 | Emitir por un **medio autorizado** (portal del SENIAT, imprenta digital, máquina fiscal o contingencia) | art. 4 | Portal web / app del SENIAT |
| 2 | **Número de control** único y consecutivo por emisor: 2 dígitos de identificador + hasta 8 secuenciales | art. 8.3, 9.1 | Campo `N° de Control` de `iducdev_ve_fiscal` (valida formato y duplicados) |
| 3 | **Número de factura** asignado por el medio de emisión | art. 9 | Campo `N° Factura Fiscal` |
| 4 | **Fecha y hora** de emisión | art. 8.5 | Campo `Fecha y hora de emisión fiscal` |
| 5 | Identificación del cliente con **RIF** | art. 8.4 | Campo NIF del contacto + etiqueta "RIF" en el PDF |
| 6 | Marca **(E)** en líneas exentas, exoneradas o no gravadas | art. 8.7 | Reporte de factura del módulo |
| 7 | **Tipo de cambio** y **total en bolívares** cuando se factura en divisa | art. 8.12 | Bloque al pie del PDF (`x_seniat_rate`, `x_ve_amount_total`) |
| 8 | Frase de emisión conforme a la Providencia | art. 19 | Bloque legal al pie del PDF |
| 9 | **Contingencia**: emitir en formatos autorizados y remitir los documentos al día siguiente | art. 7 | Medio `Formatos de contingencia` + actividad recordatorio automática |
| 10 | Las **copias** de documentos de contingencia no dan derecho a crédito fiscal | art. 11.3 | Aviso impreso en el PDF del módulo |

> Los números de artículo corresponden a la lectura del escaneo. **Verifica la
> numeración final** en el texto publicado antes de citarla en un documento
> oficial.

> **Cliente extranjero que paga en dólares:** no exime del documento fiscal;
> solo cambia el IVA (0 % por exportación, con marca `(E)`) y la identificación
> del cliente. Ver §5.1 y §6.4.

---

## 2. Calendario

| Fecha | Qué pasa | Qué hacer |
|---|---|---|
| 21/10/2026 | Publicación en Gaceta Oficial N° 43.484 | Archivar la Gaceta. Ya está en el repo. |
| 21/10/2026 – 19/04/2027 | Período de adecuación (180 días continuos) | Configurar el portal, probar el flujo completo y ajustar la contabilidad |
| **19/04/2027** | **Entrada en vigencia** | Todas las facturas nuevas deben emitirse por medio autorizado |

Recomendación de hitos internos:

- **Antes de 31/12/2026** — cuenta en el portal del SENIAT, datos de la
  empresa actualizados y una factura de prueba emitida (sin valor fiscal).
- **Antes de 28/02/2027** — flujo completo probado en una base `odoo-demo`:
  factura en borrador → emisión en portal → registro de N° de control →
  validación → PDF.
- **Antes de 31/03/2027** — decisión cerrada sobre la moneda funcional (ver
  §4) y contador revisando las alícuotas vigentes.
- **19/04/2027** — activar la casilla **"Exigir datos fiscales SENIAT al
  validar"** en Ajustes → Contabilidad.

---

## 3. Checklist de puesta en marcha

### 3.1 Cuenta y trámites en el SENIAT

- [ ] Verificar que el **RIF de IDUCDEV** está activo y con los datos
      actualizados (razón social, dirección, actividad económica).
- [ ] Verificar la **vigencia del usuario y la clave del portal** del SENIAT
      (o del servicio en línea que corresponda).
- [ ] Confirmar que la actividad económica declarada cubre **desarrollo de
      software / servicios informáticos** (afecta a la alícuota de IVA y a las
      retenciones).
- [ ] Guardar el comprobante de cada trámite en el chatter del contacto de la
      compañía o en `backups/` (fuera del repo si contiene datos sensibles).

### 3.2 Configuración de Odoo

- [ ] Compañía con **país Venezuela**, RIF, dirección y teléfono.
- [ ] `l10n_ve` instalado (plan contable e impuestos 0 / 8 / 12 / 22 %).
- [ ] `iducdev_ve_fiscal` instalado y visible en la pestaña **Otra
      información → SENIAT (Venezuela)** de la factura.
- [ ] **Alícuota de IVA confirmada** con el contador y corregida en el
      impuesto si no coincide con la que trae la localización.
- [ ] Impuesto **"Exento (exportación)"** creado al 0 %.
- [ ] RIF cargado en **todos** los contactos que vayan a recibir factura.
- [ ] Secuencia de facturas de Odoo revisada (no debe chocar con la del
      portal; son numeraciones distintas).
- [ ] Casilla **"Exigir datos fiscales SENIAT al validar"** activada solo
      cuando ya se emita por el portal.

### 3.3 Prueba de extremo a extremo

- [ ] Crear una base de prueba (`odoo-demo`) desde el gestor de bases de
      datos.
- [ ] Cliente de prueba con RIF → cotización → orden de venta → factura en
      borrador.
- [ ] Emitir la factura de prueba en el portal del SENIAT y anotar N° de
      factura, N° de control y fecha/hora.
- [ ] Registrar los datos en Odoo y **validar**.
- [ ] Comprobar en el PDF: N° de control, N° fiscal, fecha y hora, tipo de
      cambio, total en bolívares, marca `(E)` en la línea exenta y etiqueta
      RIF.
- [ ] Adjuntar el PDF del SENIAT al chatter y enviarlo al "cliente" de prueba.
- [ ] Repetir el flujo con una **nota de crédito**.
- [ ] Repetir el flujo con un **cliente extranjero**: impuesto
      `Exento (exportación)`, marca `(E)` en las líneas, total en bolívares y
      comprobar **cómo lo identifica el portal** (ID fiscal extranjero o
      "consumidor final").
- [ ] Probar el flujo de **contingencia** y comprobar que aparece la actividad
      de recordatorio.

---

## 4. Decisión pendiente: moneda funcional (D1)

Hoy la compañía está configurada en **USD**. Hay dos escenarios válidos y el
módulo funciona en ambos:

| | Opción A — libros en USD | Opción B — libros en VES |
|---|---|---|
| Moneda de la compañía | USD | VES |
| Facturar en USD | directo | con multi-moneda (Odoo convierte al tipo del día) |
| Total en bolívares en el PDF | lo calcula el módulo | ya es la moneda de la factura |
| Cambiar después | no se puede con asientos validados | no se puede con asientos validados |

**Recomendación:** confirmar con el contador si los libros deben llevarse en
bolívares (Opción B) y, si es así, migrar **antes de la primera factura
real**. Cambiar la moneda de la compañía está bloqueado en Odoo si existen
apuntes contables (`_existing_accounting`): habría que eliminar los asientos
previos, cosa que solo tiene sentido en una base de pruebas.

---

## 5. Flujo diario a partir del 19/04/2027

1. Crear la factura en Odoo y dejarla en **borrador**.
2. Emitirla en el **portal / app del SENIAT**.
3. Registrar en Odoo, pestaña **Otra información → SENIAT (Venezuela)**:
   medio de emisión, N° Factura Fiscal, N° de Control y fecha/hora.
4. Revisar el **tipo de cambio aplicado** si la factura está en divisa.
5. **Validar** la factura.
6. Adjuntar el **PDF del SENIAT** al chatter y enviarlo al cliente.
7. Registrar el pago cuando entre el dinero.

### 5.1 Cliente extranjero que paga en dólares

El hecho de que el cliente sea extranjero **no exime** del documento fiscal:
sigue necesitando N° de factura, N° de control y fecha/hora. Lo que cambia es
el tratamiento del IVA y la identificación:

1. **Exportación de servicios** → IVA **0 %** con el impuesto
   `Exento (exportación)` y marca `(E)` en las líneas (art. 8.7).
   Condiciones: cliente domiciliado fuera, servicio consumido fuera y
   facturación/cobro en divisa.
2. **Factura en USD** → el PDF muestra tipo de cambio y total en bolívares
   (art. 8.12).
3. **Identificación**: se usa el ID fiscal extranjero (EIN, VAT, pasaporte) en
   el campo NIF. En el PDF aparecerá bajo la etiqueta "RIF".
4. **Sin retenciones**: un cliente del exterior no retiene ISLR ni IVA
   venezolanos.
5. **Diferencia en cambio**: solo si los libros están en VES; Odoo la registra
   sola al conciliar el cobro.

> ⚠️ El punto a validar en el portal es la **identificación del cliente sin
> RIF venezolano**. Pruébalo en `odoo-demo` antes de abril: si el portal no
> acepta el ID extranjero, habrá que usar la opción de "consumidor final" y
> dejarlo anotado en el chatter de la factura.

Detalle operativo en [`GUIA-CLIENTE.md`](./GUIA-CLIENTE.md) §3, Paso 5-F.

---

## 6. Contingencias

### 6.1 Si el portal del SENIAT no funciona

1. Emitir en los **formatos de contingencia autorizados** (talonario físico).
2. En Odoo, poner el **Medio de emisión = Formatos de contingencia**.
3. Validar la factura: el módulo deja una **actividad** al día siguiente para
   remitir los documentos.
4. Al restablecerse el servicio, **registrar todos los documentos emitidos en
   físico** y remitirlos en PDF a la imprenta digital autorizada o a la API del
   SENIAT, **al día siguiente** (art. 7).
5. Recordar al cliente que **las copias de documentos de contingencia no dan
   derecho a crédito fiscal** (art. 11.3).

### 6.2 Si se pierde el consecutivo de números de control

- Llevar un registro externo (hoja de cálculo o el control fiscal del §7 de la
  guía) con el último N° de control emitido por el portal.
- Si el portal asigna un número repetido o salta la secuencia, **no lo
  "arregles" a mano en Odoo**: deja constancia en el chatter de la factura y
  consulta al SENIAT.
- El módulo **rechaza duplicados** por compañía; si te bloquea, es señal de
  que el número ya existe en otra factura.

### 6.3 Si el cliente no tiene RIF

- El portal del SENIAT no emite la factura fiscal sin RIF.
- No valides la factura como si estuviera emitida: pide el RIF primero, o
  emite como **consumidor final** si el portal lo permite y registra esa
  condición en el chatter.

### 6.4 Si el cliente es extranjero

- Usa su **ID fiscal del país de origen** (EIN, VAT, número de pasaporte) en el
  campo NIF del contacto.
- Si el portal no acepta ese identificador, emite como **consumidor final** o
  con el tipo de documento que ofrezca, y **deja constancia en el chatter** de
  la factura (qué documento se usó y por qué).
- No cambies el país del contacto a Venezuela para "que pase": eso rompe la
  clasificación de exportación y el tratamiento del IVA.

---

## 7. Qué NO hace este setup

- **No hay integración automática** con el portal del SENIAT ni con la API de
  una imprenta digital: los números se copian a mano.
- **No se emite el documento fiscal desde Odoo**: el PDF de Odoo es una
  **copia comercial**, no el documento válido para el crédito fiscal del
  cliente.
- **No hay firma electrónica ni código QR** de validación: los aporta el medio
  de emisión autorizado.
- **No hay libro de ventas electrónico** ni declaración automática de IVA:
  eso se hace en el portal del SENIAT o con el contador.

Si más adelante quieres automatizar la emisión, las opciones son:

1. **API de una imprenta digital autorizada** (contrato y costo mensual).
2. **Máquina fiscal** (hardware + homologación).
3. **Integración directa con la API del SENIAT** (si la publican y tu volumen
   lo justifica).

Ninguna está implementada aquí; el módulo `iducdev_ve_fiscal` está preparado
para seguir registrando los datos que devuelva cualquiera de esos medios.

---

## 8. Enlaces internos

- [`GUIA-CLIENTE.md`](./GUIA-CLIENTE.md) — flujo comercial completo.
- [`extra-addons/iducdev_ve_fiscal/README.md`](./extra-addons/iducdev_ve_fiscal/README.md)
  — instalación y uso del módulo.
- [`README.md`](./README.md) — infraestructura (Docker, respaldos, módulos).

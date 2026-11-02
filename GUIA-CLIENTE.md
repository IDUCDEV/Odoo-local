# Guía de cliente — IDUCDEV × Odoo 19 Community (local)

Playbook de ventas para **Isaac Urdaneta / IDUCDEV** ([www.iducdev.org](https://www.iducdev.org)):
cada vez que entre un cliente potencial, abre este documento y sigue el paso
que corresponda. Todo está pensado para **Odoo 19 Community en local** (tu
Docker portátil) facturando en **USD con IVA venezolano**.

- **§0** el checklist rápido (léelo siempre).
- **§1** la configuración de la base: solo la primera vez, o cuando cambie algo.
- **§2–§7** el flujo detallado cliente a cliente, plantillas, errores y fichas.

> ⚠️ Las alícuotas, secuencias y requisitos fiscales (RIF, IVA de exportación,
> etc.) pueden cambiar; esta guía te dice **dónde** configurarlo en Odoo, no
> sustituye a un contador.
>
> 🆕 **Desde el 19/04/2027** rige la Providencia SNAT/2026/00093 (Gaceta
> Oficial N° 43.484 del 21/10/2026): las facturas deben emitirse por un medio
> autorizado y llevar **número de control** y **fecha/hora de emisión**. Ver
> **[CUMPLIMIENTO-SENIAT.md](./CUMPLIMIENTO-SENIAT.md)** y §1.13.

---

## §0 Checklist rápido — un cliente nuevo en 11 pasos

1. ☐ **Contacto** — Contactos → Nuevo (razón social, **RIF obligatorio**, país, USD).
2. ☐ **Oportunidad** — CRM → Oportunidades → Nueva (con el presupuesto del lead).
3. ☐ **Cotización** — desde la oportunidad: "Crear cotización" (plantilla del servicio).
4. ☐ **Enviar** — botón "Enviar por correo" (o PDF a mano) + programar seguimiento.
5. ☐ **Confirmar** — cuando el cliente diga que sí: botón "Confirmar" → Orden de venta.
6. ☐ **Crear factura** — completa, por hitos o con anticipo (§3, Paso 5), **en borrador**.
7. ☐ **Emitir el documento fiscal** — portal web/app del SENIAT: te da el
   N° de factura fiscal y el N° de control (§1.13).
8. ☐ **Registrar y validar** — pestaña "Otra información" → SENIAT (Venezuela):
   medio, N° fiscal, N° de control y fecha/hora → **Validar**.
9. ☐ **Registrar pago** — cuando entre el dinero (banco o efectivo).
10. ☐ **Contrato** — si hay mantenimiento mensual: app Contratos (OCA).
11. ☐ **Respaldo** — `./backup.sh` al menos una vez al mes.

> **Antes de la primera factura real:** crea una base `odoo-demo` (ver README,
> gestor de bases de datos) y simula un cliente completo de principio a fin:
> contacto → cotización → hitos → **emisión fiscal** → factura → cobro. Te toma
> 20 minutos y te evita un susto con un cliente de carne y hueso.

---

## §1 Configuración única (solo la primera vez)

### 1.1 Compañía y localización fiscal (Venezuela)

1. **Instala la app CRM** si aún no está: Aplicaciones → buscar "CRM" →
   Instalar. `sale_crm` se instala solo y es el que enlaza oportunidades con
   cotizaciones. La app **Contratos** (OCA `contract`) ya la tienes en
   `extra-addons/`.
2. Ajustes → Ajustes generales → sección **Compañía**:
   - Nombre: `IDUCDEV` (o tu razón social completa).
   - **RIF**, dirección, teléfono, web (`www.iducdev.org`).
   - **País: Venezuela** ← este es el campo que dispara la localización. Al
     guardarlo Odoo te ofrecerá instalar el plan contable de Venezuela
     (`l10n_ve`): cúrrelo, trae cuentas e impuestos preconfigurados.
3. **Instala el módulo fiscal** `iducdev_ve_fiscal` (§1.13): Aplicaciones →
   Actualizar lista de aplicaciones → "Venezuela - Datos fiscales SENIAT" →
   Instalar. Añade número de control, fecha/hora de emisión, total en
   bolívares y la etiqueta RIF en los PDF.
4. **Modo desarrollador**: en la parte inferior de Ajustes → "Activar modo
   desarrollador". Necesitarás el menú Técnico para el correo y algunas
   configuraciones de esta guía.

### 1.2 Moneda: USD con control en bolívares

Hay dos formas válidas de llevar la contabilidad. **Elige una y no la cambies
después**: cambiar la moneda de la compañía con asientos ya registrados está
bloqueado en Odoo (habría que borrar los apuntes primero).

**Opción A — Libros en USD (lo que tienes hoy).** Es la más cómoda si cobras
casi todo en divisas y tu contador acepta los libros en dólares:

- Ajustes → Ajustes generales → **Moneda**: **Dólar estadounidense (USD)**.
- Activa **multi-moneda** y deja el **VES** con tipo de cambio actualizado:
  Ajustes → Contabilidad → Monedas → VES → modo **"Tasa manual"** y actualiza
  la tasa (o cárgala a mano cada vez que factures).
- Cada factura en USD muestra además, al pie, el **tipo de cambio aplicado y
  el total en bolívares** (lo pone el módulo `iducdev_ve_fiscal`, §1.13). Eso
  cubre el art. 8.12 de la Providencia.

**Opción B — Libros en VES (recomendada para cumplir sin discusiones).** Es
la moneda funcional del país y evita que el contador tenga que reconvertir
todo:

- Ajustes → Ajustes generales → **Moneda**: **Bolívar (VES)**.
- Puedes **seguir cotizando y facturando en USD**: activa multi-moneda y elige
  USD en la cotización. Odoo guarda el asiento en VES al tipo de cambio del día
  y la factura conserva el importe en dólares.

> **Pendiente de decidir (D1).** Hoy la base está en **USD (Opción A)**. Si tu
> contador pide libros en bolívares, hay que migrar a la Opción B **antes de
> emitir facturas reales**: es un cambio de configuración de la compañía, no
> de los datos, pero no se puede deshacer con apuntes ya validados.

### 1.3 Impuestos

- Ve a Facturación → Configuración → Impuestos. `l10n_ve` trae **0 %, 8 %,
  12 % y 22 %** (el 22 % viene marcado como impuesto de venta por defecto).
- ⚠️ **Verifica la alícuota con tu contador antes de facturar.** La guía
  anterior hablaba de un 16 % general; la localización instalada no lo trae.
  Si la alícuota vigente para tus servicios es otra:
  - Facturación → Impuestos → abre el impuesto → **Cantidad** → corrige el
    porcentaje → guardar. Se recalcula en las facturas nuevas, no en las ya
    validadas.
- Deja **un solo impuesto de venta por defecto** y asígnalo en los productos
  (§1.7), para no elegir impuesto en cada línea.
- Para clientes del exterior **no crees un impuesto nuevo**: `l10n_ve` ya trae
  uno al 0 % (aparece como `0% EXEMPT`, tipo **venta**). Renómbralo para que se
  entienda:
  - Facturación → Impuestos → abre `0% EXEMPT` (el de **venta**, no el de
    compra) → Nombre: `Exento (exportación)` → Cantidad: `0` → guardar.
- Úsalo **línea por línea** cuando el cliente sea del exterior (§3, Paso 5-F).
  En el PDF esas líneas saldrán marcadas con **(E)** (art. 8.7, §1.13).

### 1.4 Cuentas bancarias y efectivo

- Facturación → Configuración → **Cuentas bancarias** → Nueva: tu banco y tu
  cuenta en USD (por ejemplo Banesco/Provincial en dólares). Esto hace falta
  para registrar cobros y para que salga el IBAN en el PDF.
- Verifica también que exista el diario **Efectivo** (para pagos en efectivo
  o Zelle registrado a mano): Facturación → Configuración → Diarios.

### 1.5 Correo saliente (obligatorio para enviar cotizaciones)

Sin SMTP, el botón "Enviar por correo" no sale de Odoo. Con tu Gmail:

- Ajustes → Ajustes generales → **Correo electrónico** → "Configurar" →
  Servidores de correo salientes → Nuevo:
  - Servidor: `smtp.gmail.com`, Puerto: `465`, Seguridad: `SSL/TLS`
    (o `587` con `STARTTLS`).
  - Usuario: `iducdev.inc@gmail.com`.
  - Contraseña: una **contraseña de aplicación** de Google (no tu contraseña
    normal): Google Cuenta → Seguridad → Contraseñas de aplicaciones.
- Prueba con "Validar" y luego envíate una cotización de prueba.

### 1.6 Equipo de ventas y alias (para los leads del formulario web)

- CRM → Configuración → **Equipos de ventas** → crea `IDUCDEV`.
- En el equipo verás un **alias de correo** (por ejemplo
  `iducdev+crm@...`). Cualquier correo que llegue a esa dirección crea un
  **lead** automáticamente en el equipo. Configura en Gmail un alias/redirección
  si quieres que el formulario de tu portafolio caiga solo en el CRM; si no,
  los leads del formulario los metes a mano (§3, Paso 0).

### 1.7 Catálogo de productos (tus servicios del portafolio)

Ventas → Productos → **Nuevo**. Crea estos 5 con tipo **Servicio**:

| Código | Producto | Servicio en iducdev.org | Unidad | Política de facturación | Impuesto | Precio por defecto |
|---|---|---|---|---|---|---|
| `APP-FLUTTER` | App móvil Flutter | Desarrollo Mobile (1-3 meses) | Unidad | **Cantidades entregadas** | IVA (§1.3) | déjalo en 0, el precio va en la cotización |
| `WEB-NEXT` | Web App Next.js | Landing / Web App (1-4 sem) | Unidad | **Cantidades entregadas** | IVA (§1.3) | 0 |
| `BACK-SUPA` | Backend Supabase | Backend, APIs y BD (1-3 sem) | Unidad | **Cantidades entregadas** | IVA (§1.3) | 0 |
| `CONS-HORA` | Consultoría por hora | Asesoría técnica / arquitectura | Hora | **Cantidades entregadas** | IVA (§1.3) | tu tarifa (ej. 25 $/h) |
| `MANT-MES` | Mantenimiento mensual | Soporte Continuo post-lanzamiento | Mes | **Cantidades pedidas** | IVA (§1.3) | tu cuota (ej. 50 $/mes) |

Detalles que no te saltes:

- **Unidad de medida**: para `CONS-HORA` selecciona la unidad **Hora** (viene
  con Odoo); para los demás, **Unidad**. Nada de inventario: son servicios.
- **Política de facturación** está en la pestaña "Facturación" del producto.
  "Cantidades entregadas" es la que permite facturar por hitos (§5.B).
- Los tres servicios de proyecto van a **precio cerrado por alcance**: la
  línea lleva cantidad 1 y el precio que cotices. Las horas sueltas van con
  `CONS-HORA`.

### 1.8 Plantillas de cotización

Ventas → Configuración → **Plantillas de cotización** → Nueva. Crea tres:

1. **Proyecto Flutter** — líneas de ejemplo: `APP-FLUTTER`, `BACK-SUPA`.
2. **Web / Landing** — línea: `WEB-NEXT`.
3. **Mantenimiento** — línea: `MANT-MES` (por si prefieres cotizar el
   mantenimiento en vez de pasarlo directo a contrato).

En cada plantilla pon **Validez: 30 días**, tus condiciones generales (§4.3)
en el campo de notas/notas legales, y el texto del portal (§4.6). Así cada
cotización nueva sale armada y solo ajustas cantidades y precios.

### 1.9 Condiciones de pago

Ventas → Configuración → **Condiciones de pago**: crea `50 % anticipo / 50 %
entrega` y `Pago a la vista (15 días)`. Asígnalas al cliente en la pestaña
**Ventas** del contacto; saldrán en la cotización y en la factura.

### 1.10 Proveedor de pago (opcional, solo si quieres cobrar online)

Facturación → Configuración → **Proveedores de pago**: Stripe y PayPal vienen
en Community, pero necesitas cuenta y claves propias. Mientras tanto, el flujo
manual de "Registrar pago" (§6) siempre te vale.

### 1.11 App Compras (opcional): gastos externos y subcontratación

Si compras algo en tu nombre para un cliente (dominio, hosting, suscripción de
Diseño, un freelance puntual), instala la app **Compras** (`purchase`,
Community): Facturas de proveedor → Nueva, y listo. El gasto queda registrado
y, si quieres re-invertirlo al cliente, añade una **línea extra en la orden
de venta** del proyecto (ej. "Dominio y hosting anual — 80 $") y factúrala
con el resto. No confundas: la orden de venta es lo que **cobras**, la
compra es lo que **pagas**.

### 1.12 Lo que NO debes instalar

Inventario, RRHH, Manufactura, Sitio web, Punto de venta, Suscripciones
(Enterprise), Timesheets (no existe en Community: controla tus horas en
Toggl o una hoja de cálculo). La app **Proyecto** (`project`) sí es
Community y te puede servir para seguir tareas por cliente/hito, pero no
factura sola: la facturación sale siempre de Ventas.

### 1.13 Cumplimiento SENIAT (Providencia SNAT/2026/00093)

La **Gaceta Oficial N° 43.484 del 21/10/2026** publicó la Providencia
SNAT/2026/00093. Entra en vigencia a los **180 días continuos**, es decir el
**19 de abril de 2027**. Desde esa fecha la factura debe emitirse por un medio
autorizado y llevar número de control, número de factura, fecha y hora de
emisión, tipo de cambio y total en bolívares.

**La estrategia es la "Opción A": el documento fiscal lo emite el SENIAT, Odoo
solo lo registra.**

1. **Emite gratis por el portal del SENIAT.** La Providencia permite el
   **portal web / app del SENIAT** como medio de emisión gratuito (art. 4.1.1).
   No necesitas imprenta digital ni máquina fiscal para empezar.
2. **Instala el módulo `iducdev_ve_fiscal`** (ya está en `extra-addons/`):
   Aplicaciones → Actualizar lista → "Venezuela - Datos fiscales SENIAT" →
   Instalar. Añade a la factura una pestaña **Otra información → SENIAT
   (Venezuela)** con medio de emisión, N° Factura Fiscal, N° de Control, fecha
   y hora de emisión y tipo de cambio.
3. **Flujo por factura** (es el modo E de §3, Paso 5):
   - Crea la factura en Odoo y déjala en **borrador**.
   - Emítela en el portal del SENIAT con los mismos datos (cliente, RIF,
     líneas, IVA). El portal te devuelve **N° de factura** y **N° de control**.
   - Vuelve a Odoo y registra esos números en la pestaña **SENIAT
     (Venezuela)**, más la fecha y hora exactas.
   - **Valida** la factura y adjunta el PDF del SENIAT al chatter.
4. **Activa la exigencia cuando empieces.** Por defecto el módulo **no bloquea**
   la validación, para que puedas seguir trabajando con normalidad hasta 2027.
   Cuando ya estés emitiendo por el portal: Ajustes → Contabilidad → **"Exigir
   datos fiscales SENIAT al validar"**. Desde ahí, una factura sin número de
   control no se puede validar.
5. **Número de control**: dos dígitos de identificador + hasta ocho
   secuenciales (ej. `00 00000001`). Debe ser **único y consecutivo por
   emisor**; el módulo rechaza duplicados y formatos inválidos.
6. **Contingencia** (art. 7): si el portal no funciona, emite en los formatos de
   contingencia autorizados, marca el medio como **"Formatos de contingencia"**
   en Odoo y el módulo te deja una **actividad recordatorio** para remitir los
   documentos al día siguiente.
7. **RIF**: el módulo hace que los PDF digan **"RIF"** en vez de "Tax ID".
   Rellena el RIF en la compañía y en **todos** los contactos (§3, Paso 1).

El detalle completo (checklist, trámites, calendario y contingencias) está en
**[CUMPLIMIENTO-SENIAT.md](./CUMPLIMIENTO-SENIAT.md)**.

---

## §2 Glosario mínimo para un dev

| Término en Odoo | Qué es |
|---|---|
| **Cotización** (Quotation) | Propuesta de precio al cliente. Se puede enviar, imprimir y modificar hasta que la confirmas. |
| **Orden de venta** (SO) | Cotización **confirmada**: ya hay compromiso de compra y dispara la facturación. |
| **Factura** | Documento fiscal. En **borrador** no vale; al **Validar** cobra número (secuencia) y crea el asiento contable. |
| **N° de Control** | Numeración fiscal que exige el SENIAT (2 dígitos + hasta 8 secuenciales), distinta de la secuencia interna de Odoo. |
| **N° Factura Fiscal** | Número que asigna el medio de emisión autorizado (portal del SENIAT, imprenta digital o máquina fiscal). |
| **Medio de emisión** | Cómo se emitió el documento fiscal: portal del SENIAT, imprenta digital, máquina fiscal o formatos de contingencia. |
| **RIF** | Registro de Información Fiscal del cliente/empresa. En Odoo es el campo "NIF" del contacto. |
| **Alícuota** | Porcentaje de IVA aplicado a una línea. |
| **Exportación de servicios** | Servicio prestado desde Venezuela y consumido fuera, facturado y cobrado en divisa → IVA 0 % y marca `(E)`. |
| **Asiento** | Registro contable que genera la factura validada en el libro mayor. |
| **Secuencia** | Numeración automática (ej. `INV/2026/0001`). No la edites a mano. |
| **Anticipo** (Down payment) | Factura parcial por adelantado que luego se descuenta de la factura final. |
| **Nota de crédito** (Reembolso) | Factura negativa que anula o corrige una anterior ya validada. |
| **Política de facturación** | Regla del producto: facturar lo pedido o lo entregado. Clave para los hitos. |
| **Registrar pago** | Marcar la factura como cobrada y enlazar el pago con un diario (banco/efectivo). |
| **Conciliación bancaria** | Cruzar tus pagos registrados en Odoo con el extracto real del banco. |
| **Portal** | Vista web que el cliente abre con un enlace para ver su cotización/factura. |

---

## §3 El flujo cliente a cliente

### Paso 0 — Del formulario web a CRM

Lo que te llega del formulario de iducdev.org (email a
`iducdev.inc@gmail.com`) contiene: nombre, email, empresa, **servicio
interesado**, **presupuesto** y **timeline**. Con eso:

- CRM → Oportunidades → **Nuevo lead** (o pásalo a oportunidad directamente).
- Copia en la descripción el mensaje del formulario.
- Mapea: *servicio* → asunto de la oportunidad; *presupuesto* → **Importe
  estimado**; *timeline* → **Fecha de cierre prevista** (1-2 meses = +30 días,
  etc.). Así el pipeline te sirve de panel de ventas real.

Si prefieres automatizarlo, usa el alias del equipo de ventas (§1.6): el
correo al alias crea el lead solo.

### Paso 1 — Contacto

Contactos → Nuevo:

- **Nombre**: razón social o nombre completo del cliente.
- **RIF/NIF** en el campo de identificación fiscal (`V-12345678`,
  `J-12345678-9`, `E-…` para extranjeros). Es **obligatorio** para la factura
  fiscal (art. 8.4 de la Providencia): sin RIF el portal del SENIAT no emite.
  En el PDF sale como **RIF** gracias al módulo `iducdev_ve_fiscal`.
- **País** (Venezuela o el del exterior; de aquí sale el impuesto por
  posición fiscal).
- Email y teléfono (el email es el que usará el portal).
- Pestaña **Ventas**: condiciones de pago y vendedor por defecto (tú).
- Si una empresa tiene varias personas, crea un contacto hijo por persona y
  asígnales la empresa padre.

### Paso 2 — Oportunidad en CRM

CRM → Oportunidades → Nueva:

- **Cliente** (el contacto del Paso 1), **Asunto** ("App delivery Flutter —
  Rifame"), **Importe estimado**, **Fecha de cierre**.
- **Etapa**: usa estas cuatro (CRM → Configuración → Etapas de oportunidad
  para crearlas): `Consultoría agendada` → `Propuesta enviada` → `Negociación`
  → `Ganada` / `Perdida`.
- **Actividad**: pulsa el reloj y programa "Llamada" o "Enviar email" para la
  fecha de seguimiento. El CRM te avisa en el menú de actividades.
- Tras la consultoría gratuita de 30 min, mueve la etapa y, si hay
  presupuesto acordado, pulsa **Crear cotización**. (La consultoría gratuita
  es solo una **reunión/actividad** en el CRM: no genera cotización ni
  factura; lo único que produce es la oportunidad.)

### Paso 3 — Cotización

Se abre la cotización ya enlazada a la oportunidad y al contacto:

1. Elige tu **plantilla** (§1.8) si no vino precargada.
2. Revisa las líneas: producto, cantidad, precio. Añade un **descuento** si
   corresponde. Para proyectos, **una línea por entrega/fase** (ver §5.B).
3. **Validez** 30 días, **condiciones de pago** las del cliente.
4. En las notas va el texto de condiciones generales (§4.3).
5. **Enviar por correo** → el cliente recibe el enlace del portal; o
   **Imprimir → PDF** y mándalo tú por WhatsApp/email.
6. **Seguimiento**: si en 5 días no responde, CRM te recuerda la actividad
   que programaste.

> Ojo: en Community **no existe la firma online con un clic**. El cliente te
> dice que sí (correo/WhatsApp) y lo confirmas tú en el Paso 4.

### Paso 4 — Confirmación (cotización → orden de venta)

- Botón **Confirmar**. La cotización pasa a **Orden de venta** y aparecen los
  botones de factura.
- La oportunidad asociada se mueve sola a **Ganada**: ya tienes el histórico
  de cuánto ganas, de qué y con qué cliente.
- Si el cliente cambia montos tras confirmar, usa **Modificaciones de orden de
  venta** (botón que aparece en la SO) para dejar registro sin borrar nada.

### Paso 5 — Facturación (elige el modo)

#### A. Todo de golpe (proyectos cerrados / web small)

SO → **Crear factura** → "Facturar líneas de la orden" (completa) →
**Validar** → **Registrar pago**.

#### B. Por hitos (el caso típico de un app Flutter) — recomendada

1. En la SO, **una línea por fase** usando tus 4 fases del proceso:
   `Hito 1 · Descubrimiento`, `Hito 2 · Diseño (Figma)`, `Hito 3 ·
   Desarrollo (Flutter + Supabase)`, `Hito 4 · Lanzamiento y soporte`.
   (Para más claridad usa el producto `WEB-NEXT` o `APP-FLUTTER` y renombra
   la descripción de la línea; Odoo permite editar la descripción de cada
   línea libremente.)
2. Los productos tienen política **"Cantidades entregadas"**, así que la SO
   no factura nada todavía.
3. Cuando termines una fase, edita la línea y pon **Cantidad entregada = 1**
   (si no ves la columna, pulsa el ícono de información ✏️ de la línea).
4. **Crear factura** → solo salen las líneas entregadas → **Validar** →
   **Registrar pago**.
5. Repite con el siguiente hito. La SO queda como estado general del proyecto
   (ya entregado / por entregar).

#### C. Con anticipo (entrada de dinero antes de empezar)

- SO completa con el total → **Crear factura** → **Anticipo (porcentaje)** →
  30 % (o **Anticipo (importe fijo)** si prefieres $300 fijos) → Validar y
  cobrar. El anticipo se **descuenta automáticamente** de la factura final.
  Combina bien con el hito 1: cobras la entrada y luego facturas por entregas.

#### D. Una orden de venta por hito (proyectos con pagos muy separados)

Cada fase es su **propio** contacto-cotización-SO-factura. Más simple de leer
y de cobrar; la oportunidad del CRM puede tener varias cotizaciones asociadas.
Úsalo si cada fase se vende y se aprueba por separado.

#### E. Emisión fiscal SENIAT (aplica a los modos A, B, C y D)

Desde el **19/04/2027** toda factura de cliente tiene que estar emitida por un
medio autorizado antes de darla por buena. Con la estrategia del §1.13, cada
factura sigue este orden:

1. **Crear la factura** en Odoo como siempre (modo A, B, C o D) y dejarla en
   **borrador**. No la valides todavía.
2. **Emitirla en el portal web / app del SENIAT** con los datos del cliente
   (razón social, RIF, líneas, alícuota). El portal te da el **N° de factura
   fiscal** y el **N° de control**.
3. **Volver a Odoo** → pestaña **Otra información → SENIAT (Venezuela)**:
   - Medio de emisión → `Portal web / App SENIAT`.
   - N° Factura Fiscal → el que dio el portal.
   - N° de Control → el que dio el portal (formato `00 00000001`).
   - Fecha y hora de emisión fiscal → la del portal, **con hora**.
   - Si la factura está en USD, revisa el **tipo de cambio aplicado** (por
     defecto toma el de Odoo a la fecha de la factura; cámbialo si el portal
     usó otro).
4. **Validar** la factura. El PDF de Odoo sale con el N° de control, el N°
   fiscal, la fecha/hora, el total en bolívares y la frase legal: es tu
   **copia comercial**.
5. **Adjuntar el PDF del SENIAT** al chatter y enviar al cliente **ese**
   documento (o ambos, dejando claro cuál es el fiscal).

> El documento fiscal válido es el del SENIAT. El PDF de Odoo es la copia
> comercial y sirve para tu gestión, no para el crédito fiscal del cliente.

> Regla práctica: para un app Flutter cobra **anticipo 30-50 % + hitos** (B+C);
> para una web pequeña, **todo de golpe** (A); para mantenimiento, **contrato**
> (Paso 7).

#### F. Cliente extranjero (exportación de servicios)

Un servicio de software prestado desde Venezuela y **consumido fuera del país**
se trata como exportación: IVA **0 %** y línea marcada **(E)**. Para que aplique
deben cumplirse las tres condiciones (confírmalas con tu contador):

1. El cliente está **domiciliado en el exterior** (su dirección fiscal, no una
   filial en Venezuela).
2. El servicio se **usa o aprovecha fuera de Venezuela**.
3. Se **factura y se cobra en divisa** (USD).

Pasos:

1. **Contacto** (Paso 1): país real del cliente y su **ID fiscal extranjero**
   (EIN, VAT, pasaporte) en el campo NIF. Ojo: el PDF lo imprimirá bajo la
   etiqueta **"RIF"**, porque es la etiqueta venezolana; es correcto pero puede
   sorprender al cliente.
2. **Impuesto**: en todas las líneas, `Exento (exportación)` (§1.3). Si dejas
   el IVA general, Odoo te muestra un **aviso rojo** en la pestaña SENIAT (el
   módulo no bloquea, solo avisa).
3. **Factura en USD**: el módulo añade al pie el **tipo de cambio aplicado y el
   total en bolívares** (art. 8.12).
4. **Emisión fiscal** (modo E): el portal del SENIAT emite también documentos
   de exportación y necesitas su N° de factura y N° de control igual que
   siempre. **Prueba antes** cómo identifica el portal a un cliente sin RIF
   venezolano: puede pedir el ID fiscal extranjero o la opción "consumidor
   final".
5. **Cobro** (Paso 6): registra el pago en el diario en USD. Un cliente
   extranjero **no retiene ISLR ni IVA** venezolanos. Si el banco te cobra
   comisión, regístrala como **cargo bancario**, no como nota de crédito.
6. **Diferencia en cambio**: solo aparece si tus libros están en VES (Opción B
   de §1.2): la factura se registra a la tasa del día y el cobro a la del día
   del pago; Odoo crea solo el asiento en el diario *Exchange Difference*.

**Guarda la prueba de exportación**: contrato, factura en USD, comprobante del
pago en divisa y domicilio del cliente. Si el servicio se consume en Venezuela
(por ejemplo, una filial local del cliente), **deja de ser exportación** y
lleva IVA normal.

**Cancelación a mitad de camino**: no borres la orden de venta. Factura lo ya
entregado (§3, Paso 5-B marca las fases completadas y crea la factura), cancela las
líneas pendientes (o cancela la SO si no se entregó nada) y cierra la
oportunidad como `Perdida` con motivo. Lo que ya se cobró no se devuelve salvo
lo que digan tus condiciones generales (§4.3).

### Paso 6 — Cobro

- Facturación → Facturas → selecciona la validada → **Registrar pago**: elige
  diario (tu banco USD o Efectivo), fecha y monto real. Si el pago viene
  parcial, regístralo igual y déjalo "pendiente" hasta completarlo.
- Para conciliar con el banco: importa el extracto (Facturación →
  Conciliación bancaria) y empareja los pagos. Sin extracto, no pasa nada:
  el pago ya quedó registrado.
- Facturas emitidas a clientes del exterior: ver el **modo F del Paso 5**
  (exportación: impuesto 0 %, marca `(E)`, sin retenciones y con prueba de
  exportación guardada).
- **Retenciones (Venezuela)**: si facturas a una empresa, es muy probable que
  te **retengan ISLR** (y a veces IVA, si el cliente es gran contribuyente).
  Odoo lo modela como **impuestos de retención** (Facturación → Impuestos →
  tipo "Retención/Impuesto sobre la renta"); si `l10n_ve` ya los trae,
  úsalos, y si no, créalos con la alícuota que te indique tu contador y
  aplícalos en la factura o en la línea correspondiente. El pago se registra
  por el **monto neto** (total menos retención) y el certificado de retención
  te lo da el cliente. No lo ignores: si no lo registras, tus libros no
  cuadran con lo que realmente entra al banco.
- **Zelle / transferencia local**: regístralo igual con **Registrar pago** en
  el diario **Efectivo** (o en tu banco si ya está acreditado); si mueves el
  dinero de un diario a otro, usa el botón **Transferencias internas** de
  Facturación para no perder el rastro.
- Para enviar la factura al cliente: **Enviar por correo** (portal) o PDF por
  tu canal. Adjunta siempre el **PDF del SENIAT** (es el documento fiscal) y,
  si quieres, el PDF de Odoo como copia comercial. Activa en Ajustes →
  Facturación los **campos legales** (dirección, teléfono, RIF) si quieres que
  salgan impresos.
- **Notas de crédito**: mismo flujo que la factura. Créala en Odoo, emítela en
  el portal del SENIAT (te da su propio N° de control), registra los datos en
  la pestaña **SENIAT (Venezuela)** y valida. El módulo valida que el número
  de control no se repita.

### Paso 7 — Soporte continuo → contrato recurrente

Tu garantía de "Soporte Continuo" se puede vender como cuota mensual y
automatizarla con la app **Contratos** (OCA `contract`, ya instalada):

1. Contratos → Contratos → **Nuevo**:
   - **Cliente**: el del proyecto.
   - **Tipo**: venta. **Inicio**: primer día del mes siguiente.
   - **Periodicidad**: mensual. **Facturación**: prepago (cobra el mes
     adelantado) o pospago (cobra al mes vencido), como prefieras.
   - **Líneas**: producto `MANT-MES`, cantidad 1, precio de la cuota.
2. Guarda. **Crear facturas** (botón del contrato) genera la factura en
   borrador; **emítela en el portal del SENIAT**, registra el N° de control y
   la fecha/hora en la pestaña **SENIAT (Venezuela)**, valida y regístrale el
   pago como siempre. También puedes dejar la **tarea programada** de
   generación automática activa (Configuración → Tareas programadas →
   "Generación de facturas de contratos") para que la factura salga sola cada
   mes; revisa de vez en cuando que las facturas salgan bien y **no olvides la
   emisión fiscal de cada una** (la generación automática no emite en el
   SENIAT).
3. Cuando el cliente quiera bajar el servicio o cancelar, pon **fin** al
   contrato en su fecha de término (no lo borres: deja el histórico).

### Paso 8 — Cierre y respaldo

- Oportunidad en `Ganada` (o `Perdida` con motivo).
- Al final del mes: `./backup.sh`. Verás el respaldo en `backups/`; guárdalo
  fuera de la carpeta de vez en cuando.
- Si el cliente pide sus datos: las facturas y cotizaciones se imprimen en PDF
  desde cada registro.

---

## §4 Plantillas textuales (copiar y pegar)

### 4.1 Correo — respuesta inicial al lead del formulario

> **Asunto:** Re: tu proyecto con IDUCDEV — agendemos 30 min 🚀
>
> Hola {nombre}, ¡gracias por escribir! Soy Isaac, desarrollador Flutter
> freelance (www.iducdev.org). Vi que te interesa **{servicio}** con un
> presupuesto de **{presupuesto}**.
> ¿Agendamos una consultoría gratuita de 30 minutos para ver alcance y
> tiempos? Te dejo mi disponencia: {día1} o {día2}. Responde con el que te
> quede mejor.
> Saludo,
> Isaac — IDUCDEV

### 4.2 Correo — envío de la cotización

> **Asunto:** Cotización {N°} — {proyecto} | IDUCDEV
>
> Hola {nombre},
> Adjunto (y en este enlace: {enlace_portal}) la cotización **{N°}** para
> **{proyecto}**.
> Resumen: **{total} USD** — anticipo de {n} % y el resto por hitos
> (Diseño → Desarrollo → Lanzamiento). Vigencia: 30 días.
> Incluye {n} rondas de cambios por fase, entrega de código fuente y 30 días
> de soporte post-lanzamiento.
> ¿Te funciona? Con tu visto bueno confirmo el proyecto y arrancamos.
> Saludo,
> Isaac — IDUCDEV

### 4.3 Condiciones generales (para el campo de notas de la cotización/contrato)

> **Condiciones generales — IDUCDEV**
> 1. **Alcance**: lo cotizado es lo entregado. Funcionalidades fuera del
>    alcance se presupuestan aparte antes de implementarse.
> 2. **Cambios**: incluidos {n} rondas de ajustes por fase; cambios de alcance
>    se cotizan como horas con `CONS-HORA`.
> 3. **Pagos**: anticipo del {n} % para arrancar; hitos restantes al entregar
>    cada fase. Facturas en USD. Sin anticipo no se inicia el desarrollo.
> 4. **Plazos**: estimados a partir de la fecha del anticipo y del material
>    recibido; demoras en insumos del cliente (textos, accesos, diseños)
>    extienden el plazo en igual proporción.
> 5. **Propiedad intelectual**: al pagar la totalidad, el cliente recibe el
>    código fuente y los derechos de uso del entregado. IDUCDEV conserva el
>    derecho de mostrar el proyecto en su portafolio salvo acuerdo escrito en
>    contrario.
> 6. **Soporte**: {n} días de corrección de bugs tras el lanzamiento; luego
>    disponible como contrato mensual (`MANT-MES`).
> 7. **Confidencialidad**: la información del cliente se trata como
>    reservada.

### 4.4 Correo — confirmación de inicio

> **Asunto:** ¡Confirmado! {proyecto} arranca 🚀
>
> Hola {nombre}, perfecto. Queda confirmado el proyecto por **{total} USD**.
> Paso la factura del **anticipo ({n} % = {monto} USD)** por el portal hoy
> mismo. Cuando se acredite el pago, arranco con {primera fase} y te comparto
> el tablero/avances cada {frecuencia}.
> Saludo,
> Isaac — IDUCDEV

### 4.5 Correo — recordatorio de pago

> **Asunto:** Factura {N°} pendiente — {proyecto}
>
> Hola {nombre}, espero que todo bien. Te recuerdo la factura **{N°}** por
> **{monto} USD** (hitos {fase}), emitida el {fecha}. Si ya la pagaste,
> disculpa y ignora este mensaje. Aquí el enlace para verla:
> {enlace_portal}. Cualquier duda con el pago, dime.
> Saludo,
> Isaac — IDUCDEV

### 4.6 Mensaje del portal (texto corto que verá el cliente al abrir la cotización)

> Propuesta de desarrollo — IDUCDEV (www.iducdev.org). Incluye fases,
> plazos y condiciones en las notas. Para aprobar, respóndeme por correo o
> WhatsApp y confirmamos el inicio.

---

## §5 Errores típicos y cómo deshacerlos

| Qué pasó | Cómo se arregla |
|---|---|
| Factura **validada** con dato malo | **Reversar** (crea una nota de crédito que la anula) y crea la factura correcta. Nunca borres ni edites la secuencia. |
| Factura validada con **impuesto equivocado** (ej. IVA general a un cliente del exterior) | Nota de crédito de la factura completa y reemitir con **Exento (exportación)**. |
| Cotización que el cliente **rechazó** | En la cotización: acción ⚙ → **Cancelar**. La oportunidad va a `Perdida` con motivo. |
| SO cancelada por equivocación | No se recicla: crea una nueva cotización (el histórico se conserva). |
| **Contacto duplicado** | Contactos → selecciona los dos → fusionar (acción de agrupar/merge) o borra el malo si no tiene facturas. |
| Precio mal puesto en una SO **confirmada** | Úsalo como aprendizaje: en SO pendientes, usa "Modificaciones de orden de venta". Si ya facturaste, nota de crédito parcial por la diferencia. |
| Cobro **duplicado** (registaste el pago dos veces) | Facturación → Pagos → Reembolsar/eliminar el duplicado y conciliar de nuevo. |
| Se cayó el Odoo a mitad de validar | Entra de nuevo y revisa Facturación → Facturas: casi siempre quedó en borrador o validada; no la dupliques sin mirar. |
| Email "enviado" pero no llegó | Mira Ajustes → Técnico → Mensajes/Correo (falló el SMTP). Corrige el servidor y reenvía; o imprime el PDF. |
| Al validar sale **"falta el número de control"** | Activaste la exigencia SENIAT (§1.13). Emite primero la factura en el portal del SENIAT y registra N° de control + fecha/hora en **Otra información → SENIAT (Venezuela)**. |
| **"El número de control ya está asignado a otra factura"** | El N° de control debe ser único y consecutivo por emisor. Revisa si copiaste el número de otra factura o si el portal te dio uno repetido (vuelve a emitir). |
| **"El número de control no es válido"** | Formato: 2 dígitos de identificador + hasta 8 secuenciales (`00 00000001`). Quita letras, guiones raros o espacios internos. |
| El PDF de Odoo **no muestra** el total en bolívares | La factura está en VES (no hace falta el bloque) o el tipo de cambio quedó en 0. Revisa **Tipo de cambio aplicado** en la pestaña SENIAT y guarda. |
| Emití en **contingencia** y olvidé remitir los documentos | El módulo deja una **actividad** al día siguiente ("Remitir documento de contingencia al SENIAT/imprenta"). Revísala en el chatter de la factura. |

---

## §6 Community vs Enterprise (qué esperar)

| Necesidad | Community (tu setup) | Alternativa si la necesitas |
|---|---|---|
| Pipeline CRM, actividades, reuniones | ✅ | — |
| Cotizaciones, plantillas, órdenes de venta | ✅ | — |
| Facturación, impuestos, pagos, notas de crédito | ✅ | — |
| Anticipos y facturación por hitos manuales | ✅ (§3, Paso 5) | — |
| Contratos recurrentes | ✅ OCA `contract` | Suscripciones (Enterprise) |
| Portal del cliente y cobro online (Stripe/PayPal) | ✅ | — |
| Firma/aceptación de la cotización con un clic | ❌ | Confirmas tú manualmente |
| Márgenes/coste real de cada SO, Timesheets, minería de leads, enriquecimiento de leads | ❌ | Toggl / hojas de cálculo / prospección manual |

---

## §7 Ficha del cliente (imprimible / copiable)

```
FICHA DE CLIENTE — IDUCDEV
─────────────────────────────────────────────────
Cliente: ____________________  RIF: ____________
País: __________  Moneda: USD / VES  ¿Exportación? S / N
Contacto email: ______________  Tel: ____________
Condiciones de pago: __________  Anticipo: ____ %

SERVICIO:  App Flutter / Web Next.js / Backend Supabase / Otro: ________
PRESUPUESTO TOTAL: ________ USD
IMPUESTO:  IVA ___ % / Exento (exportación)

Contacto en Odoo: ☐ creado (Paso 1)   RIF cargado ☐
Oportunidad CRM: ☐ creada  etapa: ____________
Cotización N°: ____  enviada ☐  fecha: ________
Confirmada (SO): ☐  fecha: ________
Modo de facturación: ☐ Completa  ☐ Hitos  ☐ Anticipo+Hitos
Hito 1 (Descubrimiento) ____ USD  factura ☐  cobrada ☐
Hito 2 (Diseño)         ____ USD  factura ☐  cobrada ☐
Hito 3 (Desarrollo)     ____ USD  factura ☐  cobrada ☐
Hito 4 (Lanzamiento)    ____ USD  factura ☐  cobrada ☐
Contrato mantenimiento: ☐ creado  cuota ____ USD/mes  inicio ________
Retención (cliente empresa): ☐ ISLR ____ %   ☐ IVA ____ %
Gastos externos (app Compras): ☐ registrados  ☐ re-invertidos en la SO
Backup mensual: ☐
Notas: ________________________________________
```

### 7.1 Control fiscal por factura (SENIAT)

Rellena una fila por cada factura emitida. Sirve para cuadrar el consecutivo
con el portal del SENIAT.

```
FACTURA | Fecha/hora emisión | Medio | N° Factura Fiscal | N° de Control | Total USD | Tasa | Total VES | PDF SENIAT adjunto
________|___________________|_______|__________________|_______________|__________|______|___________|___________________
________|___________________|_______|__________________|_______________|__________|______|___________|___________________
________|___________________|_______|__________________|_______________|__________|______|___________|___________________
```

---

*Documento vivo: si algo del flujo cambia (nuevos productos, otra alícuota,
otra forma de cobrar), actualiza aquí y no en el README.*

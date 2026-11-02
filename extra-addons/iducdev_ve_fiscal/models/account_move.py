# Part of IDUCDEV. See LICENSE file for full copyright and licensing details.
import re
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

#: Dos dígitos de identificador + hasta ocho dígitos secuenciales (art. 9.1).
CONTROL_NUMBER_RE = re.compile(r"^\d{2}\d{1,8}$")

CONTINGENCY_SUMMARY = "Remitir documento de contingencia al SENIAT/imprenta"


class AccountMove(models.Model):
    _inherit = "account.move"

    # ------------------------------------------------------------------
    # Datos exigidos por la Providencia SNAT/2026/00093
    # ------------------------------------------------------------------
    x_fiscal_medium = fields.Selection(
        selection=[
            ("portal", "Portal web / App SENIAT"),
            ("imprenta", "Imprenta digital o proveedor autorizado"),
            ("maquina", "Máquina fiscal"),
            ("contingencia", "Formatos de contingencia"),
        ],
        string="Medio de emisión",
        copy=False,
        help="Medio por el que se emitió el documento fiscal (art. 4).",
    )
    x_fiscal_state = fields.Selection(
        selection=[
            ("pending", "Pendiente de emitir"),
            ("issued", "Emitida"),
            ("contingency", "Contingencia por remitir"),
            ("cancelled", "Anulada"),
        ],
        string="Estado fiscal",
        default="pending",
        copy=False,
        tracking=True,
    )
    x_fiscal_number = fields.Char(
        string="N° Factura Fiscal",
        copy=False,
        help="Número que asigna el portal del SENIAT, la imprenta digital o la "
        "máquina fiscal. Es distinto del número interno de Odoo.",
    )
    x_control_number = fields.Char(
        string="N° de Control",
        copy=False,
        help="Consecutivo y único por emisor: dos (2) dígitos de identificador "
        "y hasta ocho (8) dígitos secuenciales. Ejemplo: 00 00000001.",
    )
    x_fiscal_datetime = fields.Datetime(
        string="Fecha y hora de emisión fiscal",
        copy=False,
        help="Momento exacto de emisión del documento fiscal (art. 8.5).",
    )

    # ------------------------------------------------------------------
    # Moneda extranjera (art. 8.12)
    # ------------------------------------------------------------------
    x_seniat_rate = fields.Float(
        string="Tipo de cambio aplicado",
        digits=(16, 6),
        copy=False,
        help="Bolívares por una unidad de la moneda de la factura. Si se deja "
        "en 0 se usa el tipo de cambio configurado en Odoo a la fecha de la "
        "factura.",
    )
    x_ve_currency_id = fields.Many2one(
        "res.currency",
        string="Moneda nacional",
        default=lambda self: self.env.ref("base.VES", raise_if_not_found=False),
    )
    x_ve_amount_total = fields.Monetary(
        string="Total en bolívares",
        currency_field="x_ve_currency_id",
        compute="_compute_x_ve_amounts",
        store=True,
    )
    x_ve_rate_used = fields.Float(
        string="Tipo de cambio usado",
        digits=(16, 6),
        compute="_compute_x_ve_amounts",
        store=True,
    )

    # ------------------------------------------------------------------
    # Cómputos
    # ------------------------------------------------------------------
    @api.depends(
        "amount_total",
        "currency_id",
        "invoice_date",
        "x_seniat_rate",
        "x_ve_currency_id",
        "company_id",
    )
    def _compute_x_ve_amounts(self):
        ve_currency = self.env.ref("base.VES", raise_if_not_found=False)
        for move in self:
            target = move.x_ve_currency_id or ve_currency
            if not target or not move.currency_id:
                move.x_ve_rate_used = 0.0
                move.x_ve_amount_total = 0.0
                continue
            if move.currency_id == target:
                move.x_ve_rate_used = 1.0
                move.x_ve_amount_total = move.amount_total
                continue
            rate = move.x_seniat_rate
            if not rate:
                rate = move.currency_id._get_conversion_rate(
                    move.currency_id,
                    target,
                    move.company_id,
                    move.invoice_date or fields.Date.context_today(move),
                )
            move.x_ve_rate_used = rate
            move.x_ve_amount_total = target.round(move.amount_total * rate)

    # ------------------------------------------------------------------
    # Aviso de exportación (no bloqueante)
    # ------------------------------------------------------------------
    x_ve_tax_warning = fields.Char(
        string="Aviso fiscal",
        compute="_compute_x_ve_tax_warning",
        help="Aviso cuando el cliente es del exterior y alguna línea lleva IVA. "
        "Si el servicio es una exportación, debe ir con el impuesto "
        '"Exento (exportación)" (art. 8.7).',
    )

    @api.depends(
        "move_type",
        "partner_id.country_id",
        "invoice_line_ids.display_type",
        "invoice_line_ids.tax_ids",
        "invoice_line_ids.tax_ids.amount",
    )
    def _compute_x_ve_tax_warning(self):
        ve_country = self.env.ref("base.ve", raise_if_not_found=False)
        for move in self:
            warning = False
            country = move.partner_id.country_id
            if (
                ve_country
                and move.is_sale_document(include_receipts=False)
                and country
                and country != ve_country
            ):
                taxed_lines = move.invoice_line_ids.filtered(
                    lambda line: line.display_type == "product"
                    and any(line.tax_ids.mapped("amount"))
                )
                if taxed_lines:
                    warning = _(
                        "El cliente es de %(country)s y hay líneas con IVA. Si el "
                        'servicio es una exportación, usa el impuesto "Exento '
                        '(exportación)" para que la línea salga marcada con (E) '
                        "(art. 8.7).",
                        country=country.display_name,
                    )
            move.x_ve_tax_warning = warning

    # ------------------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------------------
    @api.constrains("x_control_number")
    def _check_x_control_number_format(self):
        for move in self:
            value = (move.x_control_number or "").replace(" ", "").replace("-", "")
            if value and not CONTROL_NUMBER_RE.match(value):
                raise ValidationError(
                    _(
                        'El número de control "%(value)s" no es válido: debe tener '
                        "dos (2) dígitos de identificador y hasta ocho (8) dígitos "
                        "secuenciales.",
                        value=move.x_control_number,
                    )
                )

    @api.constrains("x_control_number", "company_id")
    def _check_x_control_number_unique(self):
        for move in self.filtered("x_control_number"):
            duplicate = self.search_count(
                [
                    ("id", "!=", move.id),
                    ("company_id", "=", move.company_id.id),
                    ("x_control_number", "=", move.x_control_number),
                ]
            )
            if duplicate:
                raise ValidationError(
                    _(
                        'El número de control "%(value)s" ya está asignado a otra '
                        "factura de la compañía: la numeración debe ser consecutiva "
                        "y única por emisor.",
                        value=move.x_control_number,
                    )
                )

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------
    def _post(self, soft=True):
        self._check_x_ve_fiscal_requirements()
        moves = super()._post(soft=soft)
        moves._update_x_ve_fiscal_state()
        return moves

    def _check_x_ve_fiscal_requirements(self):
        """Bloquea la validación si falta el número de control (art. 8.3)."""
        for move in self:
            if not move.is_sale_document(include_receipts=False):
                continue
            if not move.company_id.x_ve_fiscal_enforcement:
                continue
            missing = []
            if not move.x_control_number:
                missing.append(_("el número de control"))
            if not move.x_fiscal_datetime:
                missing.append(_("la fecha y hora de emisión fiscal"))
            if missing:
                raise ValidationError(
                    _(
                        "No se puede validar %(name)s: falta %(missing)s.\n\n"
                        "Emita primero el documento por el medio autorizado (portal "
                        'del SENIAT, imprenta digital o formatos de contingencia) y '
                        'registre los datos en la pestaña "Otra información".',
                        name=move.display_name,
                        missing=_(" y ").join(missing),
                    )
                )

    def _update_x_ve_fiscal_state(self):
        for move in self:
            if not move.is_sale_document(include_receipts=False):
                continue
            if move.x_fiscal_medium == "contingencia":
                move.x_fiscal_state = "contingency"
                move._schedule_x_ve_contingency_reminder()
            elif move.x_control_number:
                move.x_fiscal_state = "issued"
            else:
                move.x_fiscal_state = "pending"

    def _schedule_x_ve_contingency_reminder(self):
        """Recuerda remitir al día siguiente los documentos de contingencia (art. 7)."""
        activity_type = self.env.ref(
            "mail.mail_activity_data_todo", raise_if_not_found=False
        )
        if not activity_type:
            return
        deadline = fields.Date.context_today(self) + timedelta(days=1)
        for move in self:
            already_scheduled = move.activity_ids.filtered(
                lambda activity: CONTINGENCY_SUMMARY in (activity.summary or "")
            )
            if already_scheduled:
                continue
            move.activity_schedule(
                activity_type_id=activity_type.id,
                date_deadline=deadline,
                summary=CONTINGENCY_SUMMARY,
                note=_(
                    "Artículo 7 de la Providencia SNAT/2026/00093: una vez superada "
                    "la contingencia debe registrar todos los documentos emitidos en "
                    "físico y remitirlos en PDF, al día siguiente, a la imprenta "
                    "digital autorizada o a la API del SENIAT."
                ),
            )

    def button_draft(self):
        result = super().button_draft()
        self.filtered(
            lambda move: move.x_fiscal_state in ("issued", "contingency")
        ).write({"x_fiscal_state": "pending"})
        return result

    def button_cancel(self):
        result = super().button_cancel()
        self.filtered(
            lambda move: move.x_fiscal_state != "cancelled"
        ).write({"x_fiscal_state": "cancelled"})
        return result

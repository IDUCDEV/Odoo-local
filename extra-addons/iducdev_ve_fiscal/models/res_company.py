# Part of IDUCDEV. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    x_ve_fiscal_enforcement = fields.Boolean(
        string="Exigir datos fiscales SENIAT al validar",
        default=False,
        help="Si está activo, no se podrá validar una factura o nota de crédito "
        "de cliente sin número de control y fecha/hora de emisión fiscal.\n"
        "Actívelo cuando empiece a emitir por el portal del SENIAT o por una "
        "imprenta digital autorizada.",
    )

# Part of IDUCDEV. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_ve_fiscal_enforcement = fields.Boolean(
        related="company_id.x_ve_fiscal_enforcement",
        readonly=False,
    )

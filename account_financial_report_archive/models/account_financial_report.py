# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountFinancialReport(models.Model):
    _inherit = "account.financial.report"

    active = fields.Boolean(
        default=True,
    )

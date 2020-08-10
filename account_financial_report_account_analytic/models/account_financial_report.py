# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountFinancialReport(models.Model):
    _inherit = "account.financial.report"

    account_analytic = fields.Many2one(
        comodel_name='account.analytic',
        readonly=False,
        copy=False,
        string='Account analytic',
    )

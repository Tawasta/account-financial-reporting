# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountCommonReport(models.TransientModel):
    _inherit = "accounting.report"

    account_analytic = fields.Many2one(
        comodel_name='account.analytic.account',
        readonly=False,
        copy=False,
        string='Account analytic',
    )

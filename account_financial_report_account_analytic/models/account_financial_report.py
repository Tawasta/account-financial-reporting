# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    account_analytic = fields.Many2one(
        comodel_name='account.analytic.account',
        readonly=False,
        copy=False,
        string='Account analytic',
    )

    def _build_contexts(self, data):
        result = super(AccountCommonReport, self)._build_contexts(data)
        print("===================")
        print(result)
        print("===================")
        if self.analytic_account:
            result['analytic_account'] = self.analytic_account
        return result

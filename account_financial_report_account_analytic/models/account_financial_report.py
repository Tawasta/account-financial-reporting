# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    account_analytic = fields.Many2many(
        comodel_name='account.analytic.account',
        readonly=False,
        copy=False,
        string='Account analytic',
    )

    def _build_contexts(self, data):
        result = super(AccountCommonReport, self)._build_contexts(data)
        if self.account_analytic:
            result['analytic_ids'] = self.account_analytic.mapped('id')
        #print("================")
        #print(result)
        #print("================")
        return result

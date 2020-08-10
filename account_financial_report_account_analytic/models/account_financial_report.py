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

    def _print_report(self, data):
        data['form'].update(
            self.read([
                'date_from_cmp',
                'debit_credit',
                'date_to_cmp',
                'filter_cmp',
                'account_report_id',
                'enable_filter',
                'label_filter',
                'target_move',
                'account_analytic'
            ])[0])
        return self.env['report'].get_action(
            self,
            'account.report_financial',
            data=data
        )

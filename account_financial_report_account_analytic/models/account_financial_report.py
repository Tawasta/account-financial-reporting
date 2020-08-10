# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    account_analytic = fields.Many2one(
        comodel_name='account.analytic.account',
        readonly=False,
        copy=False,
        string='Account analytic',
    )

    @api.multi
    def check_report(self):
        res = super(AccountingReport, self).check_report()
        data = {}
        data['form'] = self.read([
            'account_report_id',
            'date_from_cmp',
            'date_to_cmp',
            'journal_ids',
            'filter_cmp',
            'target_move',
            'account_analytic'
        ])[0]
        for field in ['account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(data)
        res['data']['form']['comparison_context'] = comparison_context
        return res

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

# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountingReport(models.TransientModel):

    _inherit = 'accounting.report'

    def _build_comparison_context(self, data):
        result = super(AccountingReport, self)._build_comparison_context(data)
        if self.analytic_tags:
            result['analytic_tags'] = self.analytic_tags.mapped('id')
        return result

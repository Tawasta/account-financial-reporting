# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountCommonReport(models.TransientModel):

    _inherit = "account.common.report"

    analytic_tags = fields.Many2many(
        comodel_name='account.analytic.tag',
        readonly=False,
        copy=False,
        string='Analytic tags',
    )

    def _build_contexts(self, data):
        result = super(AccountCommonReport, self)._build_contexts(data)
        if self.analytic_tags:
            result['analytic_tags'] = self.analytic_tags.mapped('id')
        return result

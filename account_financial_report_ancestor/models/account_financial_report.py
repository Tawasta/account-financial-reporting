# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountFinancialReport(models.Model):
    _inherit = "account.financial.report"

    ancestor_id = fields.Many2one(
        comodel_name='account.financial.report',
        compute='_compute_ancestor_id',
        readonly=True,
        copy=False,
        string='Ancestor',
    )

    def _compute_ancestor_id(self):
        for record in self:
            record.ancestor_id = \
                record.parent_id.ancestor_id if record.parent_id else record

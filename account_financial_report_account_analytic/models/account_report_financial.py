# -*- coding: utf-8 -*-
import time
from odoo.exceptions import UserError
from odoo import api, models, _


class ReportFinancial(models.AbstractModel):
    _inherit = "report.account.report_financial"

    def _compute_account_balance(self, accounts):
        analytic_ids = self.env.context.get('analytic_ids') or False
        """ compute the balance, debit and credit for the provided accounts
        """
        mapping = {
            'balance': "COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance",
            'debit': "COALESCE(SUM(debit), 0) as debit",
            'credit': "COALESCE(SUM(credit), 0) as credit",
        }

        res = {}
        for account in accounts:
            res[account.id] = dict((fn, 0.0) for fn in mapping.keys())
        if accounts:
            tables, where_clause, where_params = self.env['account.move.line']._query_get()
            tables = tables.replace('"', '') if tables else "account_move_line"
            wheres = [""]
            if where_clause.strip():
                wheres.append(where_clause.strip())
            filters = " AND ".join(wheres)
            if analytic_ids:
                filters = filters \
                    + " " \
                    + "AND analytic_account_id IN " \
                    + "(" \
                    + ', '.join(map(str, analytic_ids)) \
                    + ")" \
                    + " "
            request = "SELECT account_id as id, " + ', '.join(mapping.values()) + \
                " FROM " + tables + \
                " WHERE account_id IN %s " \
                + filters + \
                " GROUP BY account_id"
            params = (tuple(accounts._ids),) + tuple(where_params)
            self.env.cr.execute(request, params)
            for row in self.env.cr.dictfetchall():
                res[row['id']] = row
        return res

    @api.model
    def render_html(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_lines = self.get_account_lines(data.get('form'))

        if 'analytic_ids' in data['form']['used_context']:
            analytic_ids = data['form']['used_context']['analytic_ids']
            account_analytics = self.env['account.analytic.account'].sudo().search([]).filtered(lambda r: r.id in analytic_ids)
            data['form']['used_context']['account_analytic_names'] = account_analytics.mapped('name')
        else:
            data['form']['used_context']['account_analytic_names'] = False

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_account_lines': report_lines,
        }
        return self.env['report'].render('account.report_financial', docargs)

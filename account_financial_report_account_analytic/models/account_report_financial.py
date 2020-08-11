# -*- coding: utf-8 -*-
from odoo import models, fields


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
                    + "AND analytic_tag_ids IN " \
                    + ', '.join(map(str, analytic_ids))

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


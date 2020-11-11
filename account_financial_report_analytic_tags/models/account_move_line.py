# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    @api.model
    def _query_get(self, domain=None):
        tables, where_clause, where_params = \
            super(AccountMoveLine, self)._query_get(domain)

        tags = self.env.context.get('analytic_tags') or False

        if tags:
            where_clause += \
                """ AND (SELECT CASE WHEN EXISTS (
                        (SELECT DISTINCT ml.id FROM account_account a INNER JOIN
                        account_move_line ml ON a.id = ml.account_id INNER JOIN
                        account_analytic_tag_account_move_line_rel atml ON
                        atml.account_move_line_id = ml.id INNER JOIN
                        account_analytic_tag aat ON
                        atml.account_analytic_tag_id = aat.id
                        WHERE aat.id IN (""" +\
                        ', '.join(map(str, tags)) + """) AND 
                        ml.id = account_move_line.id)
                        )
                    THEN CAST(1 AS BOOLEAN)
                    ELSE CAST(0 AS BOOLEAN) END)"""

        return tables, where_clause, where_params

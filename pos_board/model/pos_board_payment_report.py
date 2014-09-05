# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale Board module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import tools


class pos_board_payment_report(Model):
    _name = 'pos.board.payment.report'
    _auto = False
    _table = 'pos_board_payment_report'

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'month': fields.date('Month', size=7, readonly=True),
        'total': fields.float('Total', readonly=True),
        'average': fields.float('Average', readonly=True),
        'quantity': fields.integer('Quantity', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    MIN(absl.id) AS id,
                    absl.company_id,
                    absl.journal_id,
                    absl.month,
                    SUM(absl.amount) AS total,
                    AVG(absl.amount) AS average,
                    COUNT(*) as quantity
                FROM (
                    SELECT
                        absl.id,
                        absl.journal_id,
                        absl.type,
                        absl.date,
                        absl.company_id,
                        absl.amount,
                        DATE_TRUNC('month', date::timestamp) AS month
                    FROM account_bank_statement_line AS absl
                    ) AS absl
                LEFT OUTER JOIN account_journal AS aj
                    ON aj.id = absl.journal_id
                WHERE
                    absl.journal_id IS NOT NULL
                    AND absl.type = 'customer'
                GROUP BY
                    absl.company_id,
                    absl.journal_id,
                    absl.month
                ORDER BY
                    absl.company_id,
                    absl.journal_id,
                    absl.month
        )""" % (self._table))

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale / Point Of Sale Report module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class sale_pos_report(Model):
    _name = "sale.pos.report"
    _auto = False
    _description = "Sale and Point Of Sale Analysis"
    _table_name = 'sale_pos_report'

    _LINE_TYPE = [
        ('01_invoice_sale', 'Invoice - Via Sale'),
        ('02_invoice_pos', 'Invoice - Via Point Of Sale'),
        ('03_pos_normal', 'Point of Sale - Normal'),
    ]

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'month_date': fields.date('Month Date', readonly=True),
        'line_type': fields.selection(_LINE_TYPE, 'Type', readonly=True),
        'total': fields.float('Total', digits=(16, 2), readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table_name)
        cr.execute("""
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () as id,
        *
    FROM (
/* Draft / Paid / Done Pos Order ******************************************* */
        SELECT
            month_table.month_date,
            month_table.company_id,
            '03_pos_normal' AS line_type,
            COALESCE(result.total, 0) AS total
        FROM (
            SELECT month_date, company_id
            FROM (
                SELECT
                    date(date_trunc('month', date_order)) AS month_date,
                    company_id
                FROM pos_order
                GROUP BY month_date, company_id
            UNION
                SELECT
                    date(date_trunc('month', date_invoice)) AS month_date,
                    company_id
                FROM account_invoice
                WHERE date_invoice IS NOT NULL
                GROUP BY month_date, company_id
            ) AS month_temp
            GROUP BY month_date, company_id
        ) as month_table
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_order)) AS month_date,
                sum(total) AS total
            FROM pos_order po
            INNER JOIN (
                SELECT
                    order_id,
                    sum(price_subtotal) AS total
                FROM pos_order_line
                GROUP BY order_id
            ) pol
            ON po.id = pol.order_id
            WHERE state in ('draft', 'paid', 'done')
            GROUP BY company_id, month_date
        ) as result
        ON result.company_id = month_table.company_id
        AND result.month_date = month_table.month_date

/* Invoice from Point Of Sale Module ************************************** */
    UNION
        SELECT
            month_table.month_date,
            month_table.company_id,
            '02_invoice_pos' AS line_type,
            COALESCE(total_out_invoice, 0)
                - COALESCE(total_out_refund, 0) AS total
        FROM (
            SELECT month_date, company_id
            FROM (
                SELECT
                    date(date_trunc('month', date_order)) AS month_date,
                    company_id
                FROM pos_order
                GROUP BY month_date, company_id
            UNION
                SELECT
                    date(date_trunc('month', date_invoice)) AS month_date,
                    company_id
                FROM account_invoice
                WHERE date_invoice IS NOT NULL
                GROUP BY month_date, company_id
            ) AS month_temp
            GROUP BY month_date, company_id
        ) as month_table
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                sum(amount_untaxed) total_out_invoice
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_invoice')
                AND id IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
                AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date
            ) AS result_invoice
        ON result_invoice.company_id = month_table.company_id
        AND result_invoice.month_date = month_table.month_date
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                sum(amount_untaxed) total_out_refund
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_refund')
                AND id IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
            AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date
            ) AS result_refund
            ON result_refund.company_id = month_table.company_id
            AND result_refund.month_date = month_table.month_date

/* Invoice from Sale Module ********************************************** */
    UNION
        SELECT
            month_table.month_date,
            month_table.company_id,
            '01_invoice_sale' AS line_type,
            COALESCE(total_out_invoice, 0)
                - COALESCE(total_out_refund, 0) AS total
        FROM (
            SELECT month_date, company_id
            FROM (
                SELECT
                    date(date_trunc('month', date_order)) AS month_date,
                    company_id
                FROM pos_order
                GROUP BY month_date, company_id
            UNION
                SELECT
                    date(date_trunc('month', date_invoice)) AS month_date,
                    company_id
                FROM account_invoice
                WHERE date_invoice IS NOT NULL
                GROUP BY month_date, company_id
            ) AS month_temp
            GROUP BY month_date, company_id
        ) as month_table
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                sum(amount_untaxed) total_out_invoice
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_invoice')
                AND id NOT IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
                AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date
            ) AS result_invoice
        ON result_invoice.company_id = month_table.company_id
        AND result_invoice.month_date = month_table.month_date
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                sum(amount_untaxed) total_out_refund
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_refund')
                AND id NOT IN (
                SELECT invoice_id
                FROM pos_order
                WHERE invoice_id IS NOT NULL)
            AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date
            ) AS result_refund
            ON result_refund.company_id = month_table.company_id
            AND result_refund.month_date = month_table.month_date

    ) as result_tmp
    ORDER BY month_date, company_id
)""" % (self._table_name))

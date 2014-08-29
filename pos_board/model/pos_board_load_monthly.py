# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale Board module for OpenERP
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

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import tools


class pos_board_load_monthly(Model):
    _name = 'pos.board.load.monthly'
    _description = "POS Board Load Monthly"
    _auto = False
    _log_access = False
    _columns = {
        'date': fields.date('Date'),
        'month': fields.char('Month', size=64, required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'amount_tax_excluded': fields.float('Net Sales', digits=(12, 2)),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'pos_board_load_monthly')
        cr.execute("""
            create or replace view pos_board_load_monthly as (
                SELECT
                    min(po.id) as id,
                    min(date_trunc('day',po.date_order)) as date,
                    to_char(po.date_order,'YYYY:mm') as month,
                    po.company_id AS company_id,
                    round(sum(pol.price_subtotal),2) as amount_tax_excluded
                FROM
                    pos_order po
                    INNER JOIN pos_order_line pol
                        ON po.id = pol.order_id
                WHERE
                    po.create_date > now() - 14 * interval '1 month'
                GROUP BY
                    po.company_id,
                    month
            )""")

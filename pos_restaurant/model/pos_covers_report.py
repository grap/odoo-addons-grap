# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Restaurant module for OpenERP
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


class pos_covers_report(Model):
    _name = 'pos.covers.report'
    _auto = False
    _table = 'pos_covers_report'

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'shop_id': fields.many2one(
            'sale.shop', 'Shop', readonly=True),
        'user_id': fields.many2one(
            'res.users', 'User', readonly=True),
        'day': fields.char(
            'Day', readonly=True),
        'date': fields.date(
            'Date', readonly=True),
        'week_day': fields.integer(
            'Week Day', readonly=True),
        'week': fields.char(
            'Week', readonly=True),
        'week_date': fields.char(
            'Week', readonly=True),
        'month': fields.date(
            'Month', readonly=True),
        'covers_total': fields.integer(
            'Covers Total', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    req.id,
                    req.company_id,
                    req.shop_id,
                    req.user_id,
                    req.date,
                    to_char(req.date,'YYYY/MM/DD') as day,
                    extract(dow from req.date) + 1 as week_day,
                    to_char(DATE_TRUNC('week',req.date),'YYYY/MM/DD') as week,
                    DATE_TRUNC('week',req.date) as week_date,
                    DATE_TRUNC('month',req.date) AS month,
                    req.covers_total
                FROM (
                    SELECT
                        MIN(po.id) AS id,
                        po.company_id,
                        po.shop_id,
                        po.user_id,
                        DATE_TRUNC('day',po.date_order) AS date,
                        SUM(po.covers) as covers_total
                    FROM
                        pos_order as po
                    GROUP BY
                        company_id,
                        shop_id,
                        user_id,
                        date
                    ) as req
                ORDER BY
                    date desc
        )""" % (self._table))

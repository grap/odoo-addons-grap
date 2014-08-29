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


class pos_order_report(Model):
    _inherit = 'report.pos.order'

    _columns = {
        'categ_id': fields.many2one(
            'product.category', 'Category', readonly=True),
        'categ_id2': fields.many2one(
            'product.category', 'Category2', readonly=True),
        'categ_id3': fields.many2one(
            'product.category', 'Category3', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_pos_order')
        cr.execute("""
            create or replace view report_pos_order as (
                select
                    min(l.id) as id,
                    count(*) as nbr,
                    to_date(to_char(s.date_order, 'dd-MM-YYYY'), 'dd-MM-YYYY')
                        as date,
                    sum(l.qty * u.factor) as product_qty,
                    sum(l.qty * l.price_unit) as price_total,
                    sum((l.qty * l.price_unit) * (l.discount / 100))
                        as total_discount,
                    (sum(l.qty*l.price_unit)
                        /sum(l.qty * u.factor))::decimal(16,2)
                        as average_price,
                    sum(cast(to_char(date_trunc('day',s.date_order)
                        - date_trunc('day',s.create_date),'DD') as int))
                        as delay_validation,
                    to_char(s.date_order, 'YYYY') as year,
                    to_char(s.date_order, 'MM') as month,
                    to_char(s.date_order, 'YYYY-MM-DD') as day,
                    s.partner_id as partner_id,
                    s.state as state,
                    s.user_id as user_id,
                    s.shop_id as shop_id,
                    s.company_id as company_id,
                    s.sale_journal as journal_id,
                    l.product_id as product_id,
                    pt.categ_id as categ_id,
                    pc.parent_id as categ_id2,
                    pc2.parent_id as categ_id3
                from pos_order_line as l
                    left join pos_order s on (s.id=l.order_id)
                    left join product_product pp on (pp.id=l.product_id)
                    left join product_template pt on (pt.id=pp.product_tmpl_id)
                    left join product_category pc on (pt.categ_id=pc.id)
                    left join product_category pc2 on (pc.parent_id=pc2.id)
                    left join product_uom u on (u.id=pt.uom_id)
                group by
                    to_char(s.date_order, 'dd-MM-YYYY'),
                    to_char(s.date_order, 'YYYY'),
                    to_char(s.date_order, 'MM'),
                    to_char(s.date_order, 'YYYY-MM-DD'),
                    s.partner_id, s.state, pt.categ_id, pc.parent_id,
                    pc2.parent_id, s.user_id,s.shop_id, s.company_id,
                    s.sale_journal, l.product_id, s.create_date
                having
                    sum(l.qty * u.factor) != 0)""")

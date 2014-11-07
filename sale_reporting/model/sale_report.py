# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Reporting module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


class sale_report(Model):
    _inherit = 'sale.report'

    _columns = {
        'categ_id2': fields.many2one(
            'product.category', 'Category2', readonly=True),
        'categ_id3': fields.many2one(
            'product.category', 'Category3', readonly=True),
        'total_discount': fields.float(
            'Total Discount', readonly=True),
        'average_price': fields.float(
            'Average Price', readonly=True, group_operator='avg'),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'sale_report')
        cr.execute("""
create or replace view sale_report as (
    select
        min(l.id) as id,
        l.product_id as product_id,
        t.uom_id as product_uom,
        sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
        sum(l.product_uom_qty * l.price_unit * (100.0-l.discount) / 100.0)
            as price_total,
        sum((l.product_uom_qty * l.price_unit) * (l.discount / 100))
            as total_discount,
        (sum(l.product_uom_qty*l.price_unit) / sum(l.product_uom_qty
            / u.factor * u2.factor))::decimal(16,2) as average_price,
        count(*) as nbr,
        s.date_order as date,
        s.date_confirm as date_confirm,
        to_char(s.date_order, 'YYYY') as year,
        to_char(s.date_order, 'MM') as month,
        to_char(s.date_order, 'YYYY-MM-DD') as day,
        s.partner_id as partner_id,
        s.user_id as user_id,
        s.shop_id as shop_id,
        s.company_id as company_id,
        extract(epoch from avg(date_trunc('day',s.date_confirm)
            - date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2)
            as delay,
        s.state,
        t.categ_id as categ_id,
        pc2.id as categ_id2,
        pc2.parent_id as categ_id3,
        s.pricelist_id as pricelist_id,
        s.project_id as analytic_account_id
    from
        sale_order_line l
          join sale_order s on (l.order_id=s.id)
            left join product_product p on (l.product_id=p.id)
                left join product_template t on (p.product_tmpl_id=t.id)
        left join product_category pc on (t.categ_id=pc.id)
        left join product_category pc2 on (pc.parent_id=pc2.id)
        left join product_uom u on (u.id=l.product_uom)
        left join product_uom u2 on (u2.id=t.uom_id)
    group by
        l.product_id,
        l.order_id,
        t.uom_id,
        t.categ_id,
        pc2.id,
        pc2.parent_id,
        s.date_order,
        s.date_confirm,
        s.partner_id,
        s.user_id,
        s.shop_id,
        s.company_id,
        s.state,
        s.pricelist_id,
        s.project_id
)""")

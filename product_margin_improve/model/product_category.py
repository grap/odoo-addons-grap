# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
# flake8: noqa
import time
from openerp.osv.orm import Model
from openerp.osv import fields

class product_category(Model):
    _inherit = "product.category"


    def _get_products(self, cr, uid, ids, context=None):
        res = {}
        if context is None:
            context = {}
        pp_obj = self.pool.get('product.product')
        for categ in self.browse(cr, uid, ids, context=context):
            res[categ.id] = pp_obj.search(cr, uid, [
                ('categ_id','child_of',categ.id),
                ('sale_ok','=',True),
                ], context=context)
        return res


    def _product_margin_categ(self, cr, uid, ids, field_names, arg, context=None):
#    we rewrite the product_margin._product_margin_categ function as it doesn't take
#    into account the UoM, nor the discounts on the invoices

        res = {}
        if context is None:
            context = {}
        company_id = self.pool.get('res.users').browse(cr, uid, uid,
            context=context).company_id.id
        pp_obj = self.pool.get('product.product')

        for val in self.browse(cr, uid, ids, context=context):
            value = {}
            date_from = context.get('date_from', time.strftime('%Y-01-01'))
            date_to = context.get('date_to', time.strftime('%Y-12-31'))
            invoice_state = context.get('invoice_state', 'open_verified_paid')
            value['date_from'] = date_from
            value['date_to'] = date_to
            value['invoice_state'] = invoice_state
            
            product_ids = val._get_products(context=context)
            
            fields = pp_obj.read(cr, uid, product_ids[val.id], [], context=context)
            sales_gap = 0
            purchase_gap = 0
            pos_gap = 0
            total_gap = 0
            total_li_gap = 0
            sale_income = 0
            pos_income = 0
            total_income = 0
            total_li_income = 0
            total_cost = 0
            normal_cost = 0
            total_margin = 0
            li_total_margin = 0
            expected_margin = 0
            li_expected_margin = 0
            total_sale_expected = 0
            
            for product in fields:
                sales_gap += product['sales_gap']
                purchase_gap += product['purchase_gap']
                pos_gap += product['pos_gap']
                total_gap += product['total_gap']
                total_li_gap += product['total_li_gap']
                sale_income += product['sale_income']
                pos_income += product['pos_income']
                total_income += product['total_income']
                total_li_income += product['total_li_income']
                total_cost += product['total_cost']
                normal_cost += product['normal_cost']
                total_margin += product['total_margin']
                li_total_margin += product['li_total_margin']
                expected_margin += product['expected_margin']
                li_expected_margin += product['li_expected_margin']
                total_sale_expected += product['total_sale_expected']

            expected_margin_rate = total_sale_expected and 100 * expected_margin / total_sale_expected or 0
            avg_margin_rate = total_income and 100 * total_margin / total_income or 0
            li_avg_margin_rate = total_li_income and 100 * li_total_margin / total_li_income or 0

            value.update({
                'sales_gap': sales_gap,
                'purchase_gap': purchase_gap,
                'pos_gap': pos_gap,
                'total_gap': total_gap,
                'total_li_gap': total_li_gap,
                'sale_income': sale_income,
                'pos_income': pos_income,
                'total_income': total_income,
                'total_li_income': total_li_income,
                'total_cost': total_cost,
                'total_margin': total_margin,
                'li_total_margin': li_total_margin,
                'expected_margin': expected_margin,
                'li_expected_margin': li_expected_margin,
                'expected_margin_rate': expected_margin_rate,
                'avg_margin_rate': avg_margin_rate,
                'li_avg_margin_rate': li_avg_margin_rate,
            })
            value2 = {}
            for f in value.keys():
                if f in field_names:
                    value2[f] = value[f]
            res[val.id] = value2
        return res

    _columns = {
        'date_from': fields.function(_product_margin_categ, type='date', string='Margin Date From', multi='product_margin'),
        'date_to': fields.function(_product_margin_categ, type='date', string='Margin Date To', multi='product_margin'),
        'invoice_state': fields.function(_product_margin_categ, type='selection', selection=[
                ('paid','Paid'),('verified_paid','Verified and Paid'),('open_verified_paid','Open, Verified and Paid'),('draft_open_verified_paid','Draft, Open, Verified and Paid')
            ], string='Invoice State',multi='product_margin', readonly=True),
        'pos_state': fields.function(_product_margin_categ, type='selection', selection=[
           ('done','Done'),
           ('done_paid','Done and Paid'),
           ('draft_done_paid','Draft, Done and Paid'),
        ], string='POS State',multi='product_margin', readonly=True),
        'sales_gap' : fields.function(_product_margin_categ, type='float', string='Sales Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'purchase_gap' : fields.function(_product_margin_categ, type='float', string='Purchase Gap', multi='product_margin',
            help="Normal Cost - Total Cost"),
        'pos_gap' : fields.function(_product_margin_categ, type='float', string='POS Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'total_gap' : fields.function(_product_margin_categ, type='float', string='Total Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'total_li_gap' : fields.function(_product_margin_categ, type='float', string='Total Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'sale_income' : fields.function(_product_margin_categ, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes in Sale Invoices"),
        'pos_income' : fields.function(_product_margin_categ, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes in POS"),
        'total_income' : fields.function(_product_margin_categ, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes"),
        'total_li_income' : fields.function(_product_margin_categ, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes"),
        'total_cost'  : fields.function(_product_margin_categ, type='float', string='Total Cost', multi='product_margin',
            help="Sum of Multiplication of Invoice price and quantity of Supplier Invoices "),
        'total_margin' : fields.function(_product_margin_categ, type='float', string='Total Margin', multi='product_margin',
            help="Qty Sold * Unit Margin"),
        'li_total_margin' : fields.function(_product_margin_categ, type='float', string='Total Margin', multi='product_margin',
            help="Unit Margin * Qty Sold (losses included)"),
        'expected_margin' : fields.function(_product_margin_categ, type='float', string='Expected Margin', multi='product_margin',
            help="Qty Sold * Expected Unit Margin"),
        'li_expected_margin' : fields.function(_product_margin_categ, type='float', string='Expected Margin', multi='product_margin',
            help="Expected Unit Margin * Qty Sold (loss included)"),
        'expected_margin_rate' : fields.function(_product_margin_categ, type='float', string='Expected Margin (%)', multi='product_margin',
            help="Expected margin * 100 / Expected Sale"),
        'li_expected_margin_rate' : fields.function(_product_margin_categ, type='float', string='Expected Margin (%)', multi='product_margin',
            help="Expected margin * 100 / Expected Sale (losses included)"),
        'avg_margin_rate' : fields.function(_product_margin_categ, type='float', string='Avg Margin (%)', multi='product_margin',
            help="Unit Margin / Catalog price"),
        'li_avg_margin_rate' : fields.function(_product_margin_categ, type='float', string='Avg Margin Losses Included (%)', multi='product_margin',
            help="Unit Margin (losses included) / Catalog price"),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

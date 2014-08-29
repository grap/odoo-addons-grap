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

import time
from openerp.osv.orm import Model
from openerp.osv import fields

class product_product(Model):
    _inherit = "product.product"

    def _product_margin(self, cr, uid, ids, field_names, arg, context=None):
#    we rewrite the product_margin._product_margin function as it doesn't take
#    into account the UoM, nor the discounts on the invoices

        res = {}
        if context is None:
            context = {}
        company_id = self.pool.get('res.users').browse(cr, uid, uid,
            context=context).company_id.id

        for val in self.browse(cr, uid, ids, context=context):
            value = {}
            date_from = context.get('date_from', time.strftime('%Y-01-01'))
            date_to = context.get('date_to', time.strftime('%Y-12-31'))
            invoice_state = context.get('invoice_state', 'open_verified_paid')
            value['date_from'] = date_from
            value['date_to'] = date_to
            value['invoice_state'] = invoice_state
            invoice_types = ()
            states = ()
            if invoice_state == 'paid':
                states = ('paid',)
            elif invoice_state == 'verified_paid':
                states = ('verified', 'paid')
            elif invoice_state == 'open_verified_paid':
                states = ('open', 'verified', 'paid')
            elif invoice_state == 'draft_open_verified_paid':
                states = ('draft', 'open', 'verified', 'paid')

            #Calculation of HT prices
            sale_tax_amount = 0
            for tax in val.taxes_id:
                if tax.price_include:
                    sale_tax_amount += tax.amount
            list_price_HT = val.list_price / (1 + sale_tax_amount)

            purchase_tax_amount = 0
            for tax in val.supplier_taxes_id:
                if tax.price_include:
                    purchase_tax_amount += tax.amount
            standard_price_HT = val.standard_price / (1 + purchase_tax_amount)

            #Sale Invoices
            sqlstr="""select
                sum(l.price_subtotal)/sum(nullif(l.quantity/pu.factor,0)) as avg_unit_price,
                sum(l.quantity/pu.factor) as num_qty,
                sum(l.quantity/pu.factor * (l.price_subtotal/(nullif(l.quantity/pu.factor,0)))) as total,
                sum(l.quantity/pu.factor * pt.list_price) as sale_expected,
                sum(l.quantity/pu.factor * pt.standard_price) as normal_cost
                from account_invoice_line l
                left join account_invoice i on (l.invoice_id = i.id)
                left join product_product product on (product.id=l.product_id)
                left join product_template pt on (pt.id=product.product_tmpl_id)
                left join product_uom pu on (pu.id=l.uos_id)
                where l.product_id = %s 
                and i.state in %s 
                and i.type IN %s 
                and i.company_id = %s 
                and (i.date_invoice IS NULL 
                    or (i.date_invoice>=%s and i.date_invoice<=%s))
                """
            invoice_types = ('out_invoice', 'in_refund')
            cr.execute(sqlstr, (val.id, states, invoice_types, company_id,
                                                            date_from, date_to))
            result = cr.fetchall()
            result = result and result[0] or False
            value['sale_num_invoiced'] = result and result[1] or 0.0
            value['sale_income'] = result and result[2] or 0.0
            value['sale_expected'] = result and result[3] or 0.0
            value['sale_avg_price'] = value['sale_num_invoiced'] \
                            and value['sale_income'] / \
                            value['sale_num_invoiced'] or 0
            value['sales_gap'] = value['sale_expected'] \
                                                - value['sale_income']
            value['sale_list_price'] = round(list_price_HT, 2)

            #Purchase Invoices
            invoice_types = ('in_invoice', 'out_refund')
            cr.execute(sqlstr, (val.id, states, invoice_types, company_id,
                                                            date_from, date_to))
            result = cr.fetchall()
            result = result and result[0] or False
            value['purchase_num_invoiced'] = result and result[1] or 0.0
            value['total_cost'] = result and result[2] or 0.0
            value['normal_cost'] = result and result[4] or 0.0
            value['purchase_avg_price'] = value['purchase_num_invoiced'] \
                            and value['total_cost'] / \
                            value['purchase_num_invoiced'] or 0
            value['purchase_gap'] = value['normal_cost'] - \
                                                    value['total_cost']

            #POS Orders
            pos_state = context.get('pos_state', 'done_paid')
            value['pos_state'] = pos_state
            states = ()
            if pos_state == 'done':
                states = ('done',)
            elif pos_state == 'done_paid':
                states = ('done', 'paid')
            elif pos_state == 'draft_done_paid':
                states = ('draft', 'done', 'paid')

            sqlstr="""select
                    sum(pol.qty/pu.factor) as num_qty,
                    sum(pol.qty/pu.factor * (pol.price_subtotal/(nullif(pol.qty/pu.factor,0)))) as total,
                    sum(pol.qty/pu.factor * pt.list_price) as sale_expected,
                    sum(pol.qty/pu.factor * pt.standard_price) as normal_cost
                from pos_order_line pol
                left join pos_order po on (pol.order_id = po.id)
                left join product_product product on (product.id=pol.product_id)
                left join product_template pt on (pt.id=product.product_tmpl_id)
                left join product_uom pu on (pu.id=pt.uom_id)
                where pol.product_id = %s 
                and po.state in %s 
                and po.company_id = %s 
                and (po.date_order IS NULL 
                    or (po.date_order>=%s and po.date_order<=%s))
                """
            cr.execute(sqlstr, (val.id, states, company_id, date_from, date_to))
            result = cr.fetchall()[0]
            value['pos_num_sales'] = result[0] or 0.0
            value['pos_income'] = result[1] or 0.0
            value['pos_sale_expected'] = value['pos_num_sales'] * list_price_HT or 0.0
            value['pos_avg_price'] = value['pos_num_sales'] \
                            and value['pos_income'] / \
                            value['pos_num_sales'] or 0
            value['pos_gap'] = value['pos_sale_expected'] - \
                                                    value['pos_income']
            value['pos_list_price'] = round(list_price_HT, 2)

            #Total Sales
            value['total_num_sales'] = value['pos_num_sales'] \
                                            + value['sale_num_invoiced']
            value['total_income'] = value['pos_income'] \
                                            + value['sale_income']
            value['total_sale_expected'] = value['pos_sale_expected'] \
                                            + value['sale_expected']
            value['total_avg_price'] = value['total_num_sales'] and \
                    value['total_income'] / value['total_num_sales']
            value['total_gap'] = value['total_sale_expected'] - value['total_income']
            value['total_list_price'] = round(list_price_HT, 2)

            #Margin (losses excluded)
            value['expected_margin'] = value['total_num_sales'] * \
                (list_price_HT - standard_price_HT)
            value['expected_margin_rate'] = value['total_sale_expected'] and value['expected_margin'] * 100 / value['total_sale_expected'] or 0.0
            value['expected_unit_margin'] = list_price_HT - standard_price_HT
            value['unit_margin'] = value['total_avg_price'] - value['purchase_avg_price']
            value['total_margin'] = value['total_num_sales'] * value['unit_margin']
            value['avg_margin_rate'] = value['unit_margin'] * 100 / list_price_HT or 0.0

            #Inventory Losses
            sl_obj = self.pool.get('stock.location')
            inv_sl_ids = sl_obj.search(cr, uid,
                            [('usage', '=', 'inventory')], context=context)
            int_sl_ids = sl_obj.search(cr, uid,
                            [('usage', '=', 'internal')], context=context)
            
            states = ('waiting', 'assigned', 'done', 'confirmed')
            
            sqlstr = """select
                sum(sm.product_qty/pu.factor) as num_qty
                from stock_move sm
                left join product_product pp on (pp.id=sm.product_id)
                left join product_uom pu on (pu.id=sm.product_uom)
                where sm.product_id = %s and sm.state in %s 
                and (sm.date IS NULL or (sm.date>=%s and sm.date<=%s)) 
                and location_id in %s and location_dest_id in %s 
                and sm.company_id = %s
                """
            cr.execute(sqlstr, (val.id, states, date_from, date_to,
                        tuple(int_sl_ids), tuple(inv_sl_ids), company_id))
            result = cr.fetchall()[0]
            value['inventory_losses'] = result[0] or 0.0
            
            cr.execute(sqlstr, (val.id, states, date_from, date_to,
                        tuple(inv_sl_ids), tuple(int_sl_ids), company_id))
            result = cr.fetchall()[0]
            value['inventory_losses'] -= result[0] or 0.0

            #Total Sales (losses included)
            value['total_li_num_sales'] = value['total_num_sales'] \
                + value['inventory_losses']
            value['total_li_sale_expected'] = value['total_li_num_sales'] > 0 \
                and value['total_li_num_sales'] * list_price_HT or 0
            value['total_li_avg_price'] = value['total_li_num_sales'] > 0 and \
                    value['total_income'] / value['total_li_num_sales'] or False
            value['total_li_income'] = value['total_income']
            value['total_li_gap'] = value['total_li_num_sales'] > 0 and \
                value['total_li_income'] - value['total_li_sale_expected'] or \
                False
            value['total_li_list_price'] = round(list_price_HT, 2)

            #Margin (losses included)
            value['li_expected_margin'] = value['total_li_num_sales'] > 0 and \
                value['total_li_num_sales'] * (list_price_HT - 
                standard_price_HT) or 0
            value['li_expected_unit_margin'] = list_price_HT - standard_price_HT
            value['li_unit_margin'] = value['total_li_num_sales'] > 0 and \
                value['total_li_avg_price'] - value['purchase_avg_price'] or False
            value['li_total_margin'] = value['total_li_num_sales'] > 0 and \
                value['total_li_num_sales'] * (value['total_li_avg_price'] - 
                value['purchase_avg_price']) or 0
            value['li_expected_margin_rate'] = not(value['total_li_sale_expected']) \
                and 0.0 or value['total_li_num_sales'] > 0 and \
                value['expected_margin'] * 100 / value['total_li_sale_expected'] or 100
            value['li_avg_margin_rate'] = value['total_li_num_sales'] > 0 and \
                value['li_unit_margin'] * 100 / list_price_HT or 100
        
            value2 = {}
            for f in value.keys():
                if f in field_names:
                    value2[f] = value[f]
            res[val.id] = value2
        return res

    _columns = {
        'date_from': fields.function(_product_margin, type='date', string='Margin Date From', multi='product_margin'),
        'date_to': fields.function(_product_margin, type='date', string='Margin Date To', multi='product_margin'),
        'invoice_state': fields.function(_product_margin, type='selection', selection=[
                ('paid','Paid'),('verified_paid','Verified and Paid'),('open_verified_paid','Open, Verified and Paid'),('draft_open_verified_paid','Draft, Open, Verified and Paid')
            ], string='Invoice State',multi='product_margin', readonly=True),
        'pos_state': fields.function(_product_margin, type='selection', selection=[
           ('done','Done'),
           ('done_paid','Done and Paid'),
           ('draft_done_paid','Draft, Done and Paid'),
        ], string='POS State',multi='product_margin', readonly=True),
        'pos_list_price': fields.function(_product_margin, type='float',
            string='POS Sale Price', help="Catalog Price.", multi='product_margin'),
        'sale_list_price': fields.function(_product_margin, type='float',
            string='Invoice Sale Price', help="Catalog Price.", multi='product_margin'),
        'total_list_price': fields.function(_product_margin, type='float',
            string='Total Sale Price', help="Catalog Price.", multi='product_margin'),
        'total_li_list_price': fields.function(_product_margin, type='float',
            string='Sale Price (loss included)', help="Catalog Price.", multi='product_margin'),
        'sale_avg_price' : fields.function(_product_margin, type='float', string='Avg. Sale Unit Price', multi='product_margin',
            help="Avg. Price in Sales."),
        'purchase_avg_price' : fields.function(_product_margin, type='float', string='Avg. Purchase Unit Price', multi='product_margin',
            help="Avg. Price in Supplier Invoices "),
        'pos_avg_price' : fields.function(_product_margin, type='float', string='Avg. POS Unit Price', multi='product_margin',
            help="Avg. Price in POS"),
        'total_avg_price' : fields.function(_product_margin, type='float', string='Avg. Sale Unit Price', multi='product_margin',
            help="Avg. Sale Price"),
        'total_li_avg_price' : fields.function(_product_margin, type='float',
            string='Avg. Sale Unit Price (losses included)', multi='product_margin',
            help="Total Income / Qty Sold (losses included)"),
        'sale_num_invoiced' : fields.function(_product_margin, type='float', string='Qty Sold', multi='product_margin',
            help="Sum of Quantity Sold in Sale Orders"),
        'purchase_num_invoiced' : fields.function(_product_margin, type='float', string='Qty Purchased', multi='product_margin',
            help="Sum of Quantity Purchased"),
        'pos_num_sales' : fields.function(_product_margin, type='float', string='Qty Sold', multi='product_margin',
            help="Sum of Quantity Sold in POS"),
        'total_num_sales' : fields.function(_product_margin, type='float', string='Qty Sold', multi='product_margin',
            help="Sum of all Quantity Sold"),
        'inventory_losses' : fields.function(_product_margin, type='float', string='Inventory Losses', multi='product_margin',),
        'total_li_num_sales' : fields.function(_product_margin, type='float', string='Qty Sold', multi='product_margin',
            help="Sum of all Quantity Sold + Inventory losses"),
        'sales_gap' : fields.function(_product_margin, type='float', string='Sales Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'purchase_gap' : fields.function(_product_margin, type='float', string='Purchase Gap', multi='product_margin',
            help="Normal Cost - Total Cost"),
        'pos_gap' : fields.function(_product_margin, type='float', string='POS Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'total_gap' : fields.function(_product_margin, type='float', string='Total Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'total_li_gap' : fields.function(_product_margin, type='float', string='Total Gap', multi='product_margin',
            help="Expected Sale - Income"),
        'sale_income' : fields.function(_product_margin, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes in Sale Invoices"),
        'pos_income' : fields.function(_product_margin, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes in POS"),
        'total_income' : fields.function(_product_margin, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes"),
        'total_li_income' : fields.function(_product_margin, type='float', string='Income' ,multi='product_margin',
            help="Sum of real incomes"),
        'total_cost'  : fields.function(_product_margin, type='float', string='Total Cost', multi='product_margin',
            help="Sum of Multiplication of Invoice price and quantity of Supplier Invoices "),
        'sale_expected' :  fields.function(_product_margin, type='float', string='Expected Sale', multi='product_margin',
            help="Sum of Multiplication of Sale Catalog price and quantity sold"),
        'pos_sale_expected' :  fields.function(_product_margin, type='float', string='POS Expected Sale', multi='product_margin',
            help="Sum of Multiplication of Sale Catalog price and quantity sold"),
        'total_sale_expected' :  fields.function(_product_margin, type='float', string='Total Expected Sale', multi='product_margin',
            help="Sum of Multiplication of Sale Catalog price and quantity sold"),
        'total_li_sale_expected' :  fields.function(_product_margin, type='float',
            string='Total Expected Sale', multi='product_margin',
            help="Sum of Multiplication of Sale Catalog price and quantity sold (loss included)"),
        'normal_cost'  : fields.function(_product_margin, type='float', string='Normal Cost', multi='product_margin',
            help="Sum of Multiplication of Cost price and quantity of Supplier Invoices"),
        'unit_margin' : fields.function(_product_margin, type='float', string='Unit Margin', multi='product_margin',
            help="Avg. Sale Price - Avg. Purchase Price"),
        'li_unit_margin' : fields.function(_product_margin, type='float', string='Unit Margin', multi='product_margin',
            help="Avg. Sale Price (losses included) - Avg. Purchase Price"),
        'total_margin' : fields.function(_product_margin, type='float', string='Total Margin', multi='product_margin',
            help="Qty Sold * Unit Margin"),
        'li_total_margin' : fields.function(_product_margin, type='float', string='Total Margin', multi='product_margin',
            help="Unit Margin * Qty Sold (losses included)"),
        'expected_unit_margin' : fields.function(_product_margin, type='float', string='Expected Unit Margin', multi='product_margin',
            help="Catalog Price - Standard Price"),
        'li_expected_unit_margin' : fields.function(_product_margin, type='float', string='Expected Unit Margin', multi='product_margin',
            help="Catalog Price - Standard Price"),
        'expected_margin' : fields.function(_product_margin, type='float', string='Expected Margin', multi='product_margin',
            help="Qty Sold * Expected Unit Margin"),
        'li_expected_margin' : fields.function(_product_margin, type='float', string='Expected Margin', multi='product_margin',
            help="Expected Unit Margin * Qty Sold (loss included)"),
        'expected_margin_rate' : fields.function(_product_margin, type='float', string='Expected Margin (%)', multi='product_margin',
            help="Expected margin * 100 / Expected Sale"),
        'li_expected_margin_rate' : fields.function(_product_margin, type='float', string='Expected Margin (%)', multi='product_margin',
            help="Expected margin * 100 / Expected Sale (losses included)"),
        'avg_margin_rate' : fields.function(_product_margin, type='float', string='Avg Margin (%)', multi='product_margin',
            help="Unit Margin / Catalog price"),
        'li_avg_margin_rate' : fields.function(_product_margin, type='float', string='Avg Margin (%)', multi='product_margin',
            help="Unit Margin (losses included) / Catalog price"),
    }

    _defaults = {
        'invoice_state': 'open_verified_paid'
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

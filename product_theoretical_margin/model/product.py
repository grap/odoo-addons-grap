# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields


class product_product(Model):
    _name = 'product.product'
    _inherit = 'product.product'

    # compute theoretical margin
    def _compute_theoretical_margin(self, list_price, standard_price,
                                                                    tax_amount):
        if list_price !=0:
            return round(100 * (
                float(list_price) - float(standard_price) * (1 + tax_amount)
                ) / float(list_price), 2)
        else:
            return None

    # --- Return margin depending of liste_price and standard_price
    def _get_theoretical_margin(self, cr, uid, ids, field_name, arg,
                                                                context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context):
            amount = 0
            for tax in product.taxes_id:
                if tax.price_include:
                    amount += tax.amount
            res[product.id] = self._compute_theoretical_margin(
                            product.list_price, product.standard_price, amount)
        return res

     # --- Overloading create
    def create(self, cr, uid, vals, context=None):
        tax_obj = self.pool.get('account.tax')
        amount = 0
        if vals.get('taxes_id',False):
            for tax_id in vals['taxes_id'][0][2]:
                tax = tax_obj.browse(cr, uid, tax_id)
                if tax.price_include:
                    amount += tax.amount
        list_price = vals.get('list_price', 0)
        standard_price = vals.get('standard_price', 0)
        vals['theoretical_margin'] = self._compute_theoretical_margin(
                                            list_price, standard_price, amount)
        
        return super(product_product, self).create(cr, uid, vals, context)
        
    # --- Columns
    _columns = {
        'theoretical_margin': fields.function(_get_theoretical_margin,
                type='float', string='Theoretical Margin', help="""Compute the 
                theoretical margin of a product, using this formule: 
                (sale price HT - standard price HT) / sale price HT.""",
            store={
                "product.product": (lambda self,cr,uid,ids,context=None: ids, 
                    [
                        'list_price', 
                        'standard_price', 
                        'taxes_id',
                    ], 10)}
        ),
    }

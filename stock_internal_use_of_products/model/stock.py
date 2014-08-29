# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from openerp.osv import fields, osv

class stock_move(osv.osv):
    _inherit = "stock.move"

    def _get_reference_accounting_values_for_valuation(self, cr, uid, move, context=None):
        tax_obj = self.pool.get('account.tax')
        obj_product = move.product_id
        
        reference_amount, reference_currency_id = super(stock_move, self)._get_reference_accounting_values_for_valuation(cr, uid, move, context=context)
        
        reference_amount = move.product_qty * tax_obj.compute_all(cr, uid, obj_product.supplier_taxes_id, obj_product.standard_price, 1, obj_product.id, False)['total']
        
        return reference_amount, reference_currency_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

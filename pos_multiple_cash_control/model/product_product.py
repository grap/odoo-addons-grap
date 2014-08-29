# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class product_product(Model):
    _inherit = 'product.product'
    
    ### Constraint section 
    def _check_pos_ok_res_group(self, cr, uid, ids, context=None):
        ru_obj = self.pool.get('res.users')
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt) 
                    and not ru_obj.has_group(cr, uid, 'account.group_account_manager')):
                return False
        return True

    def _check_purchase_sale_pos_ok(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt) and (pp.sale_ok or pp.purchase_ok)):
                return False
        return True

    def _check_pos_purchase_tax(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt)):
                for at in pp.supplier_taxes_id:
                    if not at.price_include:
                        return False
        return True

    def _check_pos_ok_standard_price(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt) and not pp.standard_price):
                return False
        return True

    def _check_pos_property_account_expense(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if (pp.expense_pdt and not pp.property_account_expense):
                return False
        return True

    def _check_pos_property_account_income(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if (pp.income_pdt and not pp.property_account_income):
                return False
        return True

    _constraints = [
        (_check_pos_ok_res_group, "You can not create an POS expense or income product if you're not account manager !", ['expense_pdt', 'income_pdt']),
        (_check_purchase_sale_pos_ok, "You can not create a product that is both salable or purchasable and POS expense or income product !", ['expense_pdt', 'income_pdt', 'sale_ok', 'purchase_ok']),
        (_check_pos_purchase_tax, "You can not create an POS expense or income product with taxes defined with price excluded !", ['expense_pdt', 'income_pdt', 'supplier_taxes_id']),
        (_check_pos_ok_standard_price, "You can not create an POS expense or income product with a null standard price !", ['expense_pdt', 'income_pdt', 'standard_price']),
        (_check_pos_property_account_expense, "You can not create an POS expense product without account expense !", ['expense_pdt', 'income_pdt', 'property_account_expense']),
        (_check_pos_property_account_income, "You can not create an POS income product without account income !", ['expense_pdt', 'income_pdt', 'property_account_expense']),
    ]

    ### Overload Section
    def create(self, cr, uid, data, context=None):
        imd_obj = self.pool.get('ir.model.data')
        if data.get('expense_pdt', False) or data.get('income_pdt', False):
            data['type'] = 'service'
            data['uom_id'] = data['uom_po_id'] = imd_obj.get_object(cr, uid, 'product', 'product_uom_unit').id
            if data.get('expense_pdt', False):
                data['categ_id'] = imd_obj.get_object(cr, uid, 'pos_multiple_cash_control', 'cat_expense_product').id
            else:
                data['categ_id'] = imd_obj.get_object(cr, uid, 'pos_multiple_cash_control', 'cat_income_product').id
        res = super(product_product, self).create(cr, uid, data, context=context)
        return res

#------------------pas compris à quoi sert le product_ids
#    def write(self, cr, uid, ids, vals, context=None):
#        product_ids = []
#        if vals.get('property_account_expense', False): 
#            for pp in self.browse(cr, uid, ids, context=context):
#                if (pp.expense_pdt or pp.income_pdt): 
#                    product_ids.append(pp.id)
#        res = super(product_product, self).write( cr, uid, ids, vals, context=context)
        return res

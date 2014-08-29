# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import Model

class product_category(Model):
    _inherit = 'product.category'
    
    _PRODUCT_CATEGORY_PROPERTY_LIST = [
        'property_stock_journal',
        'property_stock_account_input_categ',
        'property_stock_account_output_categ',
        'property_stock_valuation_account_id',
        'property_account_income_categ',
        'property_account_expense_categ',
    ]

    ### Custom Function
    def _propagate_properties_to_childs(self, cr, uid, ids, vals, context=None):
        values = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            if property_name in vals.keys():
                values[property_name] = vals[property_name]
        if values: 
            for pc in self.browse(cr, uid, ids, context=context):
                child_ids = [x.id for x in pc.child_id]
                self.write(cr, uid, child_ids, values, context=context)

#    ### Overwrite Section
    def create(self, cr, uid, vals, context=None):
        category_id = super(product_category, self).create(cr, uid, vals, context=context)
        self._propagate_properties_to_childs(cr, uid, [category_id], vals, context=context)
        return category_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(product_category, self).write(cr, uid, ids, vals, context=context)
        self._propagate_properties_to_childs(cr, uid, ids, vals, context=context)
        return res

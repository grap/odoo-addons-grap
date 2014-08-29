# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from openerp.osv import fields, osv

class product_product(osv.osv):
    _inherit = "product.product"

    def get_product_income_expense_accounts(self, cr, uid, product_id, context=None):
        """ To get the income and expense accounts related to product.
        @param product_id: product id
        @return: dictionary which contains information regarding income and expense accounts
        """
        if context is None:
            context = {}
        categ = self.pool.get('product.product').browse(cr, uid, product_id, context=context).categ_id
        product = self.browse(cr, uid, product_id, context=context)

        income_acc = product.property_account_income and product.property_account_income.id or False
        if not income_acc:
            income_acc = categ.property_account_income_categ and categ.property_account_income_categ.id or False

        expense_acc = product.property_account_expense and product.property_account_expense.id or False
        if not expense_acc:
            expense_acc = categ.property_account_expense_categ and categ.property_account_expense_categ.id or False

        return {
            'account_income': income_acc,
            'account_expense': expense_acc,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

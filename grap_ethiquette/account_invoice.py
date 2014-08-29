# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields
import time
from openerp.report import report_sxw
from openerp.tools.translate import _

class account_invoice_line(Model):
    _inherit = 'account.invoice.line'

    ### Columns section
    def _get_extra_food_info(self, cr, uid, ids, name, arg, context=None):
        """Return extra information about food for invoices"""
        res = {}
        if context is None:
            context = {}
        for ail in self.browse(cr, uid, ids, context=context):
            res[ail.id] = ""
            product = ail.product_id
            if product: 
                # Add country name
                if product.ethiquette_origin_country: 
                    res[ail.id] += _(" - Country : ") + product.ethiquette_origin_country.name
                # Add country name
                if product.ethiquette_category: 
                    res[ail.id] +=_(" - Category : ") + product.ethiquette_category
                count_label = 0
                for label in product.ethiquette_label_ids:
                    if label.mandatory_on_invoice:
                        if count_label == 0:
                            count_label += 1
                            res[ail.id] += _(" - Label : ")
                        res[ail.id] += label.name

        return res

    _columns = {
            'extra_food_info': fields.function(_get_extra_food_info, type="char", string='Extra information for invoices'), 
        }

#### Ca c'est vraiment moche, et c'est de la duplication de code du au fait que la reference au rml est ecrit deux fois 
#### dans le code d'OpenERP de base.

#class account_invoice(Model):
#    name= 'account.invoice'
#    _inherit = 'account.invoice'

#    def invoice_print(self, cr, uid, ids, context=None):
#        print "invoice_print overload"
#        res = super(account_invoice, self).invoice_print(cr, uid, ids, context=None)
#        return {
#            'type': 'ir.actions.report.xml',
#            'report_name': 'account.invoice.food',
#            'datas': res['datas'],
#            'nodestroy' : True
#        }


#class account_invoice_food(report_sxw.rml_parse):
#    def __init__(self, cr, uid, name, context):
#        super(account_invoice_food, self).__init__(cr, uid, name, context=context)
#        self.localcontext.update({
#            'time': time,
#        })

#report_sxw.report_sxw(
#    'report.account.invoice.food',
#    'account.invoice',
#    'addons/grap_ethiquette/report/account_print_invoice.rml',
#    parser=account_invoice_food
#)

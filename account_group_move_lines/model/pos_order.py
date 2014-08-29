# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class pos_order(osv.osv):
    _inherit = "pos.order"
    
    def _get_key(self, cr, uid, data_type, values, context=None):
        key = False
        if data_type == 'product':
            key = ('product', values['tax_code_id'], values['debit'] > 0)
            values.update({
                'name' : "various products",
            })
        elif data_type == 'tax':
            key = ('tax', values['tax_code_id'], values['debit'] > 0)
        elif data_type == 'counter_part':
            key = ('counter_part', values['account_id'], values['debit'] > 0)
        return key

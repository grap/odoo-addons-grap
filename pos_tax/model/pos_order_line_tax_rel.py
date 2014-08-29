# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields, osv
from openerp.osv.orm import Model


class pos_order_line_tax_rel(Model):
    _name = 'pos.order.line.tax.rel'

    ### Columns section
    _columns = {
        'tax_id': fields.many2one('account.tax', 'Tax', required=True, ),
        'orderline_id': fields.many2one('pos.order.line', 'Order Line', required=True, ),
        'baseHT': fields.float("Base HT"),
        'amount_tax': fields.float("Tax Amount"),
    }

    ### Defaults section
    _defaults = {
        'baseHT': 0.0,
        'amount_tax': 0.0,
    }

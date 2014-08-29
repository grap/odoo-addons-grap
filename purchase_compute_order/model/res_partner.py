# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class res_partner(Model):
    _inherit="res.partner"
    
    ### Constant Values
    _target_type = [
        ('product_price_inv', '€'),
        ('time', 'days'),
        ('weight_net', 'kg'),
    ]

    _columns = {
        'purchase_target': fields.integer("Purchase Target"),
        'target_type': fields.selection(_target_type, 'Target Type', required=True,
            help='''This defines the amount of products you want to purchase. \n 
            The system will compute a purchase order based on the stock you have and the average consumption of each product.
            Target type '€': computed purchase order will cost at least the amount specified 
            Target type 'days': computed purchase order will last at least the number of days specified (according to current average consumption)
            Target type 'kg': computed purchase order will weight at least the weight specified'''),
    }

    _defaults = {
        'target_type': 'product_price_inv'
    }

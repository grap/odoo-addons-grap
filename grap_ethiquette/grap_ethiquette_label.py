# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields

class grap_ethiquette_label(Model):
    _description='Labels'
    _name = 'grap.ethiquette.label'
    _columns = {
        'short_name': fields.char('Short name', required=True, size=32),
        'name': fields.char('Name', required=True, size=64),
        'logo': fields.binary('Logo'),
        'active': fields.boolean('Active', help="By unchecking the active field you can disable a label without deleting it."),
        'mandatory_on_invoice': fields.boolean('Mandatory on invoice', help="By checking this field, the label will be printed on all the customers invoices."),
        'minimum_social_notation': fields.integer('Minimum Social Notation'),
        'minimum_local_notation': fields.integer('Minimum Local Notation'),
        'minimum_organic_notation': fields.integer('Minimum Organic Notation'),
        'minimum_packaging_notation': fields.integer('Minimum Packaging Notation'),
    }
    _defaults = {
        'active': True,
        'mandatory_on_invoice': False,
    }

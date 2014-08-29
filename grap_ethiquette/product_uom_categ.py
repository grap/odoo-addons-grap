from openerp.osv.orm import Model
from openerp.osv import fields

class product_uom_categ(Model):
    _name = 'product.uom.categ'
    _inherit = 'product.uom.categ'

    # --- Columns
    _columns = {
        'ethiquette_printable': fields.boolean('Print on ethiquette'),
    }

# -*- coding: utf-8 -*-

from openerp.osv.orm import Model


class product_template(Model):
    _inherit = "product.template"

    _defaults = {
        'uom_id': False,
        'uom_po_id': False,
    }

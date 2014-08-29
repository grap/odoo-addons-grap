# -*- coding: utf-8 -*-
from openerp.osv.orm import TransientModel
from openerp.osv import fields


class grap_ethiquette_print_wizard(TransientModel):
    _name = 'grap.ethiquette.print.wizard'
    _description = 'Labels to print'
    _rec_name = 'offset'

    def _get_default_wizard_line_ids(self, cr, uid, context=None):
        res = []
        product_ids = self.pool.get('product.product').search(cr, uid, [
            ('ethiquette_edition_state', 'in', ['1', '2']),],
            order='ethiquette_edition_state desc',
            limit=14,
            )
        for product_id in product_ids:
            res.append((0, 0, {
                'product_id': product_id,
                'quantity': 1,
                'print_unit_price': True,
                }))
        return res

    # --- Columns
    _columns = {
        'offset': fields.integer('Offset : Label number not to print', required=True),
        'border': fields.boolean('Design a border for labels'),
        'wizard_line_ids': fields.one2many('grap.ethiquette.print.wizard.line', 'wizard_id', 'Products list'),
    }

    # --- Default values
    _defaults = {
        'border': True,
        'offset': 0,
        'wizard_line_ids': _get_default_wizard_line_ids,
    }


class grap_ethiquette_print_wizard_line(TransientModel):
    _name = "grap.ethiquette.print.wizard.line"
    _description = "Information about a product to print"
    _rec_name = 'product_id'

    # --- Columns
    _columns = {
        'wizard_id': fields.many2one('grap.ethiquette.print.wizard', 'Wizard Reference', select=True),
        'product_id': fields.many2one('product.product', 'Product', required=True, help="Product to print"),
        'quantity': fields.integer('Quantity', required=True),
        'print_unit_price': fields.boolean('Print unit price'),
    }

    # --- Default values
    _defaults = {
        'quantity': 1,
        'print_unit_price': True,
    }

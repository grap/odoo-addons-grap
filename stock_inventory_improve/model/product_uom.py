# -*- coding: utf-8 -*-

import inspect #see http://docs.python.org/3/library/inspect.html for more info about the inspect module
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class product_uom(osv.osv):
    _inherit = 'product.uom'
    
    def _compute_qty_obj(self, cr, uid, from_unit, qty, to_unit, context=None):
        if context is None:
            context = {}
        if from_unit.category_id.id <> to_unit.category_id.id:
            if context.get('raise-exception', True):
                mystack = inspect.stack()
                name = False
                try:
                    product_id = mystack[1][0].f_locals['product_id']
                    product = self.pool.get('product.product').browse(
                        cr, uid, product_id, context=context
                        )
                    name = product.name
                except:
                    try:
                        name = mystack[4][0].f_locals['move'].product_id.name
                    except:
                        pass
                if name:
                    raise osv.except_osv(_('''Conversion error for product "%s"!''') % (name), _('''The UoM defined here (%s) doesn't belong the same category as the Uom defined in the Product form (%s).''') % (from_unit.name,to_unit.name,))
        return super(product_uom, self)._compute_qty_obj(cr, uid, from_unit, qty, to_unit, context=context)

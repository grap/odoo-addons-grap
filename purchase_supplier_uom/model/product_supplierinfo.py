# -*- encoding: utf-8 -*-
###############################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
###############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import SUPERUSER_ID


class product_supplierinfo(Model):
    _inherit = 'product.supplierinfo'

#Columns section
    def _get_uom(self, cr, uid, context=None):
        return context and context.get('uom_id', False)

    def _get_product_uom(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for psi in self.browse(cr, uid, ids, context=context):
            res[psi.id] = psi.product_uom_stored.id
        return res

    def _set_product_uom(self, cr, uid, ids, field_name, field_value,
                        arg, context):
        psi = self.browse(cr, uid, ids, context=context)
        psi.write({'product_uom_stored': field_value})
        return ids

    _columns = {
        'product_uom': fields.function(_get_product_uom,
                        fnct_inv=_set_product_uom, type="many2one",
                        relation="product.uom",
                        help="The supplier UoM for this product."),
        'product_uom_stored': fields.many2one('product.uom',
                    "Supplier Unit of Measure", 
                    help="This comes from the product form."),
    }

    _defaults = {
        'product_uom': _get_uom
    }

#Constraints section
    def _check_uom(self, cursor, user, ids, context=None):
        for psi in self.browse(cursor, user, ids, context=context):
            if psi.product_uom_stored and \
                    psi.product_uom_stored.category_id.id != \
                    psi.product_id.uom_po_id.category_id.id:
                return False
        return True

    _constraints = [
        (_check_uom, 'Error: The product purchase Unit of Measure and the \
        supplier purchase UOM must be in the same category.', ['uom_id']),
    ]

#Init section
    def _init_seller_uom(self, cr, uid, ids=None, context=None):
        psi_ids = self.search(cr, SUPERUSER_ID, [], context=context)
        for psi in self.browse(cr, SUPERUSER_ID, psi_ids, context=context):
            uom_id = psi.product_id.uom_po_id.id
            self.write(cr, SUPERUSER_ID, psi.id, {'product_uom': uom_id},
                        context=context)
        return psi_ids

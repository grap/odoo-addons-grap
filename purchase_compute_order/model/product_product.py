# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields
from openerp.osv.orm import Model

class product_product(Model):
    _inherit = 'product.product'

    ### Functions columns section
    def _get_draft_incoming_qty_column(self, cr, uid, ids, fields, arg, context=None):
        return self._get_draft_incoming_qty(cr, uid, ids, fields, arg, context=context)


    def _get_draft_outgoing_qty_column(self, cr, uid, ids, fields, arg, context=None):
        return self._get_draft_outgoing_qty(cr, uid, ids, fields, arg, context=context)

    _columns = {
        'draft_incoming_qty': fields.function(_get_draft_incoming_qty_column, type='float', string='Draft Incoming'),
        'draft_outgoing_qty': fields.function(_get_draft_outgoing_qty_column, type='float', string='Draft Outgoing'),
    }
    
    ### Private section
    def _get_draft_incoming_qty(self, cr, uid, ids, fields, arg, context=None):
        """ Compute incoming qty of products in draft purchase order.
            You can overload this function, in glue module.
        """
        res = {}
        pol_obj = self.pool.get('purchase.order.line')
        pol_ids = pol_obj.search(cr, uid, [('state','=','draft'), ('product_id','in',ids)], context=context)
        draft_qty = {}

        for pol in pol_obj.browse(cr, uid, pol_ids, context=context):
            draft_qty.setdefault(pol.product_id.id, 0)
            draft_qty[pol.product_id.id] += pol.product_qty / pol.product_uom.factor * pol.product_id.uom_id.factor

        for pp in self.browse(cr, uid, ids, context=context):
            res[pp.id] = draft_qty.get(pp.id, 0)
        return res

    def _get_draft_outgoing_qty(self, cr, uid, ids, fields, arg, context=None):
        """ empty function.
            Please Overload this function, in glue module.
        """
        res = {}
        for pp in self.browse(cr, uid, ids, context=context):
            res[pp.id] = 0
        return res

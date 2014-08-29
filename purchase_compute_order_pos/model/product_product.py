# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import Model
from openerp.osv import fields

class product_product(Model):
    _inherit = 'product.product'

    ### Private section
    def _get_draft_outgoing_qty(self, cr, uid, ids, fields, arg, context=None):
        """ empty function.
            Please Overload this function, in glue module.
        """
        res = super(product_product, self)._get_draft_outgoing_qty(cr, uid, ids, fields, arg, context=context)
        pol_obj = self.pool.get('pos.order.line')
        pol_ids = pol_obj.search(cr, uid, [('state','=','draft'), ('product_id','in',ids)], context=context)
        draft_qty = {}

        for line in pol_obj.browse(cr, uid, pol_ids, context=context):
            draft_qty.setdefault(line.product_id.id, 0)
            draft_qty[line.product_id.id] -= line.qty 
        for pp in self.browse(cr, uid, ids, context=context):
            res.setdefault(pp.id, 0)
            res[pp.id] += draft_qty.get(pp.id, 0)
        return res

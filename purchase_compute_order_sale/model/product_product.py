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
        sol_obj = self.pool.get('sale.order.line')
        sol_ids = sol_obj.search(cr, uid, [('state','=','draft'), ('product_id','in',ids)], context=context)
        draft_qty = {}

        for line in sol_obj.browse(cr, uid, sol_ids, context=context):
            draft_qty.setdefault(line.product_id.id, 0)
            if line.product_uos:
                draft_qty[line.product_id.id] -= line.product_uos_qty / line.product_uos.factor * line.product_id.uom_id.factor
            else:
                draft_qty[line.product_id.id] -= line.product_uom_qty / line.product_uom.factor * line.product_id.uom_id.factor
        for pp in self.browse(cr, uid, ids, context=context):
            res.setdefault(pp.id, 0)
            res[pp.id] += draft_qty.get(pp.id, 0)
        return res

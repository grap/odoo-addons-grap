# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _

class product_category(Model):
    _inherit = 'product.category'
    _rec_name = 'complete_name'

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=80):
        ids = []
        ids = self.search(cr, uid,[('complete_name', operator, name)] + args, limit=limit, context=context)
        return self.name_get(cr, uid, ids)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for pc in self.browse(cr, uid, ids):
            res.append((pc.id, pc.complete_name))
        return res

    def _compute_complete_name(self, cr, uid, id, context=None):
        pc = self.browse(cr, uid, id, context=context)
        if pc.parent_id:
            res = self._compute_complete_name(cr, uid, pc.parent_id.id, context=context) + ' / ' + pc.name
        else:
            res = pc.name
        return res

    def _get_complete_name(self, cr, uid, ids, fields, args, context=None):
        res = []
        for pc in self.browse(cr, uid, ids, context=context):
            res.append((pc.id, self._compute_complete_name(cr, uid, pc.id, context=context)))
        return dict(res)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        assert False

    ### Columns section
    _columns = {
        'complete_name': fields.function(_get_complete_name, type="char", string='Name', store=True, ),
    }

    def write(self, cr, uid, ids, values, context=None):
        res = super(product_category, self).write(cr, uid, ids, values, context=context)
        for pc in self.browse(cr, uid, ids, context=context):
            for pc_child in pc.child_id:
                self.write(cr, uid, [pc_child.id], {'complete_name': self._compute_complete_name(cr, uid, pc_child.id, context=context)}, context=context)
        return res

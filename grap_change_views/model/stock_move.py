# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class StockMove(Model):
    _inherit = 'stock.move'

    # Field Functions Section
    def _get_workflow_description(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        for move in self.browse(cr, uid, ids, context=context):
            res[move.id] = move.location_id.name + ' >> '\
                + move.location_dest_id.name
        return res

    # Column Section
    _columns = {
        'workflow_description': fields.function(
            _get_workflow_description, type='char',
            string='Workflow Description'),
    }

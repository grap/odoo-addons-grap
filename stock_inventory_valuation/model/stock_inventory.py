# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields, osv
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp

class stock_inventory(Model):
    _inherit = "stock.inventory"

    ### Columns section

    def _get_lines(self, cr, uid, ids, context=None):
        sil_obj = self.pool.get('stock.inventory.line')
        sil = sil_obj.browse(cr, uid, ids, context=context)
        res = [s.inventory_id.id for s in sil]
        return res

    def _valuation(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids, context=context):
            val = 0
            for line in inv.inventory_line_id:
                val += line.valuation
            res[inv.id] = val
        return res

    _columns = {
        'valuation': fields.function(_valuation, string='Valuation',
                        digits_compute = dp.get_precision('Product Price'),
                        store=False),
    }

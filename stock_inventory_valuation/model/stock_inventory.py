# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Inventory - Valuation Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp


class stock_inventory(Model):
    _inherit = 'stock.inventory'

    # Columns section
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
        'valuation': fields.function(
            _valuation, string='Valuation',
            digits_compute=dp.get_precision('Product Price'),
            store=False),
    }

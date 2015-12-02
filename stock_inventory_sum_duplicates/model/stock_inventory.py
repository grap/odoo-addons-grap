# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Inventory - Sum Duplicates for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class stock_inventory(Model):
    _inherit = 'stock.inventory'

    # Private Section
    def _get_keys(self, cr, uid, id, context=None):
        """This function return a list of keys / item mentioning duplicates
        in stock.inventory lines.
        key : (product_id, location_id, prod_lit_id);
        value : {
            'inventory_line_ids': [x, y],
            'qty': {uom_id_1: sum_qty_1, uom_id_2: sum_qty_2}}
        """
        inventory = self.browse(cr, uid, id, context=context)
        res = {}

        for line in inventory.inventory_line_id:
            key = (
                line.product_id.id,
                line.location_id.id,
                line.prod_lot_id.id,
            )
            res.setdefault(key, {'qty': {}, 'ids': []})
            res[key]['qty'].setdefault(line.product_uom.id, 0)
            res[key]['qty'][line.product_uom.id] += line.product_qty
            res[key]['ids'] += [line.id]

        return res

    # Computed Section
    def _get_duplicates(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for inventory in self.browse(cr, uid, ids, context=context):
            line_ids = []
            tmp = self._get_keys(cr, uid, inventory.id, context=context)
            for k, v in tmp.items():
                if len(v['ids']) > 1:
                    line_ids += v['ids']
            res[inventory.id] = {
                'duplicates_qty': len(line_ids),
                'duplicates_ids': line_ids,
            }
        return res

    _columns = {
        'duplicates_qty': fields.function(
            _get_duplicates, string='Duplicates Qty', type='float',
            multi='duplicates'),
        'duplicates_ids': fields.function(
            _get_duplicates, string='Duplicates Items',
            type='one2many', relation='stock.inventory.line',
            multi='duplicates'),
    }

    # View Section
    def action_merge_duplicates(self, cr, uid, ids, context=None):

        product_obj = self.pool['product.product']
        line_obj = self.pool['stock.inventory.line']
        uom_obj = self.pool['product.uom']
        for inventory in self.browse(cr, uid, ids, context=context):

            lines = self._get_keys(cr, uid, inventory.id, context=context)
            for key in lines.keys():
                (product_id, location_id, prod_lot_id) = key
                product_uom = product_obj.browse(
                    cr, uid, [product_id], context=context
                )[0].product_tmpl_id.uom_id
                if len(lines[key]['ids']) > 1:
                    line_obj.unlink(
                        cr, uid, lines[key]['ids'], context=context)
                    amount = 0
                    for uom in lines[key]['qty'].keys():
                        from_uom = uom_obj.browse(
                            cr, uid, [uom], context=context)[0]
                        amount += uom_obj._compute_qty_obj(
                            cr, uid, from_uom, lines[key]['qty'][uom],
                            product_uom, context=context)
                    values = {
                        'inventory_id': inventory.id,
                        'location_id': location_id,
                        'product_id': product_id,
                        'product_uom': product_uom.id,
                        'product_qty': amount,
                        'prod_lot_id': prod_lot_id,
                    }
                    line_obj.create(cr, uid, values, context=context)
        return True

    # Overload Section
    def action_confirm(self, cr, uid, ids, context=None):
        for inventory in self.browse(cr, uid, ids, context=context):
            if inventory.duplicates_qty:
                raise except_osv(
                    _("Duplicates in '%s'!") % (inventory.name),
                    _(
                        "You can not confirm this inventory because there are"
                        " %d duplicates lines in it.\n Please fix first this"
                        " lines, merging quantities.") % (
                            inventory.duplicates_qty))
        return super(stock_inventory, self).action_confirm(
            cr, uid, ids, context=context)

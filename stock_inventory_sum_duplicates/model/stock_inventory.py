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

from openerp.osv import osv


class stock_inventory(osv.osv):
    _inherit = 'stock.inventory'
    _order = 'id desc'

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        inv_line_obj = self.pool.get('stock.inventory.line')
        uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')

        for inv in self.browse(cr, uid, ids, context=context):
            lines = {}

            for line in inv.inventory_line_id:
                key = (
                    line.product_id.id,
                    line.location_id.id,
                    line.prod_lot_id.id,
                )
                product_qty = line.product_qty
                product_uom = line.product_uom.id

                # copy the inventory.lines line by line in a new dict,
                # merging the duplicates
                lines.setdefault(key, {'qty': {}, 'ids': []})
                lines[key]['qty'].setdefault(product_uom, 0)
                lines[key]['qty'][product_uom] += product_qty
                lines[key]['ids'] += [line.id]

            # browse the new dict to find the duplicates, unlink the old
            # lines and create a unique new one
            for key in lines.keys():
                (product_id, location_id, prod_lot_id) = key
                product_uom = product_obj.browse(
                    cr, uid, [product_id], context=context
                )[0].product_tmpl_id.uom_id
                if len(lines[key]['ids']) > 1:
                    inv_line_obj.unlink(
                        cr, uid, lines[key]['ids'], context=context)
                    amount = 0
                    for uom in lines[key]['qty'].keys():
                        from_uom = uom_obj.browse(
                            cr, uid, [uom], context=context)[0]
                        amount += uom_obj._compute_qty_obj(
                            cr, uid, from_uom, lines[key]['qty'][uom],
                            product_uom, context=context)
                    values = {
                        'inventory_id': inv.id,
                        'location_id': location_id,
                        'product_id': product_id,
                        'product_uom': product_uom.id,
                        'product_qty': amount,
                        'prod_lot_id': prod_lot_id,
                    }
                    inv_line_obj.create(cr, uid, values, context=context)
                else:
                    # if the line is not a duplicate,
                    # we still check the uom to prevent latter errors
                    amount = 0
                    for uom in lines[key]['qty'].keys():
                        from_uom = uom_obj.browse(
                            cr, uid, [uom], context=context)[0]
                        amount += uom_obj._compute_qty_obj(
                            cr, uid, from_uom, lines[key]['qty'][uom],
                            product_uom, context=context)

        return super(stock_inventory, self).action_confirm(
            cr, uid, ids, context=context)

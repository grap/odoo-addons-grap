# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm

class stock_inventory(osv.osv):
    _inherit = "stock.inventory"
    _name = "stock.inventory"
    _order = "id desc"

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        inv_line_obj = self.pool.get('stock.inventory.line')
        uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')

        for inv in self.browse(cr, uid, ids, context=context):
            lines = {}
            lines_to_unlink = []
            lines_to_create = {}

            for line in inv.inventory_line_id:
                key = (
                    line.product_id.id,
                    line.location_id.id,
                    line.prod_lot_id.id
                    )
                product_qty = line.product_qty
                product_uom = line.product_uom.id

                #copy the inventory.lines line by line in a new dict, merging the duplicates
                lines.setdefault(key, {'qty': {}, 'ids': []})
                lines[key]['qty'].setdefault(product_uom, 0)
                lines[key]['qty'][product_uom] += product_qty
                lines[key]['ids'] += [line.id]

            #browse the new dict to find the duplicates, unlink the old lines and create a unique new one
            for key in lines.keys():
                (product_id, location_id, prod_lot_id) = key
                product_uom = product_obj.browse(cr, uid, [product_id], 
                        context = context)[0].product_tmpl_id.uom_id
                if len(lines[key]['ids']) > 1:
                    inv_line_obj.unlink(cr, uid, 
            lines[key]['ids'],
            context = context)
                    amount = 0
                    for uom in lines[key]['qty'].keys():
                        from_uom = uom_obj.browse(cr, uid, [uom], context = context)[0]
                        amount += uom_obj._compute_qty_obj(cr, uid, from_uom, 
        lines[key]['qty'][uom],
        product_uom, context=context)
                    values = {
                        'inventory_id': inv.id,
                        'location_id': location_id,
                        'product_id': product_id,
                        'product_uom': product_uom.id,
                        'product_qty': amount,
                        'prod_lot_id': prod_lot_id,
                            }
                    inv_line_obj.create(cr, uid, values, context = context)
                else: #if the line is not a duplicate, we still check the uom to prevent latter errors
                    amount = 0
                    for uom in lines[key]['qty'].keys():
                        from_uom = uom_obj.browse(cr, uid, [uom], context = context)[0]
                        amount += uom_obj._compute_qty_obj(cr, uid, from_uom, 
        lines[key]['qty'][uom],
        product_uom, context=context)

        return super(stock_inventory, self).action_confirm(cr, uid, ids, context=context)

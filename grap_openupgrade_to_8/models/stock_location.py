# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class stock_location(Model):
    _inherit = 'stock.location'

    def set_zero_to_all_products(self, cr, uid, ids, context=None):
        product_obj = self.pool['product.product']
        inventory_obj = self.pool['stock.inventory']
        ctx = context.copy()
        ctx['active_test'] = False
        for location in self.browse(cr, uid, ids, context=context):
            ctx['location'] = location.id
            line_vals = []
            product_ids = product_obj.search(cr, uid, [], context=ctx)
            for product in product_obj.browse(
                    cr, uid, product_ids, context=ctx):
                if product.qty_available > 0.0:
                    line_val = {
                        'product_id': product.id,
                        'product_qty': 0,
                        'product_uom': product.uom_id.id,
                        'location_id': location.id,
                    }
                    line_vals.append([0, 0, line_val])

            if line_vals:
                # create inventory
                inventory_obj.create(cr, uid, {
                    'company_id': location.company_id.id,
                    'name': "Nettoyage Emplacement obsolete - %s" % (
                        location.name),
                    'inventory_line_id': line_vals,
                }, context=context)
        return True

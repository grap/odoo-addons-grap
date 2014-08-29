# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields, osv
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp

class stock_inventory_line(Model):
    _inherit = "stock.inventory.line"

    ### Columns section

    def _valuation(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_unit * line.product_qty
        return res

    _columns = {
        'price_unit': fields.float('Unit Price',
            digits_compute = dp.get_precision('Product Price'),
            help="""Technical field used to record the product cost at 
                            the time of the inventory"""),
        'valuation': fields.function(_valuation, string='Valuation', store=True,
                        digits_compute = dp.get_precision('Product Price')),
    }

    ### Defaults section
    _defaults = {
        'price_unit': 0
    }

    ### View Section
    def on_change_product_id(self, cr, uid, ids, location_id, product,
                                            uom=False, to_date=False):
        result = super(stock_inventory_line, self).on_change_product_id(cr, uid,
                    ids, location_id, product, uom=uom, to_date=to_date)
        if not product:
            return result

        product_obj = self.pool.get('product.product')
        prod = product_obj.browse(cr, uid, product)
        result['value']['price_unit'] = prod.standard_price

        return result

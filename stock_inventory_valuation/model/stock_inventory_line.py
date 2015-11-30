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


class stock_inventory_line(Model):
    _inherit = 'stock.inventory.line'

    # Columns section
    def _get_valuation(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_unit * line.product_qty
        return res

    _columns = {
        'price_unit': fields.float(
            'Unit Price', digits_compute=dp.get_precision('Product Price'),
            help="""Technical field used to record the product cost at"""
            """ the time of the inventory"""),
        'valuation': fields.function(
            _get_valuation, string='Valuation (VAT Excl)', store=True,
            digits_compute=dp.get_precision('Product Price')),
    }

    # Defaults section
    _defaults = {
        'price_unit': 0
    }

    # View Section
    def on_change_product_id(
            self, cr, uid, ids, location_id, product, uom=False,
            to_date=False):
        result = super(stock_inventory_line, self).on_change_product_id(
            cr, uid, ids, location_id, product, uom=uom, to_date=to_date)
        if not product:
            return result

        product_obj = self.pool.get('product.product')
        prod = product_obj.browse(cr, uid, product)
        result['value']['price_unit'] = prod.standard_price

        return result

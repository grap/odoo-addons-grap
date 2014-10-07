# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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


class product_product(Model):
    _inherit = 'product.product'

    _ESHOP_STATE_SELECTION = [
        ('available', 'Available for Sale'),
        ('disabled', 'Disabled'),
        ('unavailable', 'Unavailable for Sale'),
    ]

    # Field function Section
    def _get_eshop_state(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context=context):
            if not pp.eshop_category_id:
                res[pp.id] = 'unavailable'
            elif pp.eshop_ok:
                res[pp.id] = 'available'
            else:
                res[pp.id] = 'disabled'
        return res

    # Columns Section
    _columns = {
        'eshop_category_id': fields.many2one(
            'eshop.category', 'eShop Category', domain=[
                ('type', '=', 'normal')]),
        'eshop_ok': fields.boolean('Can be Sold on eShop'),
        'eshop_state': fields.function(
            _get_eshop_state, type='selection', string='eShop Stat',
            selection=_ESHOP_STATE_SELECTION, store={
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['eshop_category_id', 'eshop_ok'], 10)}),
        'eshop_minimum_qty': fields.float(
            'Minimum Quantity for eShop', required=True),
        'eshop_rounded_qty': fields.float(
            'Rounded Quantity for eShop', required=True),
    }

    # Defaults Section
    _defaults = {
        'eshop_ok': False,
        'eshop_minimum_qty': 1,
        'eshop_rounded_qty': 1,
    }

    # Constraints Section
    def _check_eshop_category(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if not pp.eshop_category_id and pp.eshop_ok:
                return False
        return True

    _constraints = [
        (_check_eshop_category,
            """Error ! You must set an eshop category if you want this"""
            """ product can be sold on eShop.""",
            ['eshop_category_id', 'eshop_ok']),
    ]

    # View Section
    def onchange_sale_ok(self, cr, uid, ids, sale_ok):
        if not sale_ok:
            return {'value': {'eshop_ok': False}}
        return {}

    def onchange_eshop_category_id(self, cr, uid, ids, eshop_category_id):
        if not eshop_category_id:
            return {'value': {'eshop_ok': False}}
        return {}

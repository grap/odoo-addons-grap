# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Inventory Improve Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

import inspect
from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class product_uom(Model):
    _inherit = 'product.uom'


    # TODO FIXME
#    # Overload Section
#    def _compute_qty_obj(self, cr, uid, from_unit, qty, to_unit, context=None):
#        if context is None:
#            context = {}
#        if from_unit.category_id.id != to_unit.category_id.id:
#            if context.get('raise-exception', True):
#                mystack = inspect.stack()
#                name = False
#                try:
#                    product_id = mystack[1][0].f_locals['product_id']
#                    product = self.pool.get('product.product').browse(
#                        cr, uid, product_id, context=context)
#                    name = product.name
#                except:
#                    try:
#                        name = mystack[4][0].f_locals['move'].product_id.name
#                    except:
#                        pass
#                if name:
#                    raise osv.except_osv(
#                        _("Conversion error for product '%s'!") % (name),
#                        _("""The UoM defined here (%s) doesn't belong the"""
#                            """ same category as the Uom defined in the"""
#                            """ Product form (%s).""") % (
#                            from_unit.name, to_unit.name,))
#        return super(product_uom, self)._compute_qty_obj(
#            cr, uid, from_unit, qty, to_unit, context=context)

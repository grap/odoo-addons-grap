# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Print Product module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class print_product_wizard(TransientModel):
    _name = 'print.product.wizard'

    # Fields Function Section
    def _get_print_type_id(self, cr, uid, context=None):
        ppt_obj = self.pool['print.product.type']
        ppt_ids = ppt_obj.search(
            cr, uid, [], limit=1, order='sequence desc, id', context=context)
        if ppt_ids:
            return ppt_ids[0]
        else:
            return False

    def _get_product_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    _columns = {
        'print_type_id': fields.many2one(
            'print.product.type', required=True, string='Print Configuration'),
        'product_id': fields.many2one(
            'product.product', readonly=True, required=True, string='Product'),
    }

    # Default values Section
    _defaults = {
        'print_type_id': _get_print_type_id,
        'product_id': _get_product_id,
    }

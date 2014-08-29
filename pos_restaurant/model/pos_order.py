# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Restaurant module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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


class pos_order(Model):
    _inherit = 'pos.order'

    # Columns section
    _columns = {
        'table_id': fields.many2one(
            'pos.table', 'Table',
            groups="pos_restaurant.res_group_restaurant_user",
            help="select the table where the customers is."),
        'covers': fields.integer(
            'Covers', groups="pos_restaurant.res_group_restaurant_user",
            help="Covers in a restaurant"),
    }

    # Overload section
    def create_from_ui(self, cr, uid, orders, context=None):
        """Overload function to save table_id and covers"""
        # Call Parent function to save new orders
        order_ids = super(pos_order, self).create_from_ui(
            cr, uid, orders, context=context)

        orders_saved = self.read(
            cr, uid, order_ids, ['pos_reference'], context=context)

        # Save extra information related to restaurants
        for order_saved in orders_saved:
            for o in orders:
                if o['data']['name'] == order_saved['pos_reference']:
                    order = o['data']
            if list(set(['table_id', 'covers']) & set(order.keys())):
                vals = {
                    'table_id': order.get('table_id', False),
                    'covers': order.get('covers', 0)}
                super(pos_order, self).write(
                    cr, uid, [order_saved['id']], vals, context=context)

        return order_ids

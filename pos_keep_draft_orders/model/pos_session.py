# -*- encoding: utf-8 -*-
##############################################################################
#
#    POS Keep Draft Orders module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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

from osv import osv


class pos_session(osv.osv):
    _inherit = 'pos.session'

    # Overload Section
    def _confirm_orders(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('pos.order')
        for session in self.browse(cr, uid, ids, context=context):
            for order in session.order_ids:
                if order.state == 'draft':
                    order_obj.write(
                        cr, uid, order.id, {'session_id': None},
                        context=context)
        return super(pos_session, self)._confirm_orders(cr, uid, ids, context)

    def create(self, cr, uid, values, context=None):
        order_obj = self.pool.get('pos.order')
        session_id = super(pos_session, self).create(cr, uid, values, context)
        order_ids = order_obj.search(
            cr, uid, [('state', '=', 'draft'), ('user_id', '=', uid)],
            context=context)
        order_obj.write(
            cr, uid, order_ids, {'session_id': session_id}, context=context)
        return session_id

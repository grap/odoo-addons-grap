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


class pos_order(osv.osv):
    _inherit = 'pos.order'

    def _default_session(self, cr, uid, context=None):
        return super(pos_order, self)._default_session(
            cr, uid, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        d = {
            'session_id': self._default_session(cr, uid, context=context),
        }
        d.update(default)
        return super(pos_order, self).copy(cr, uid, id, d, context=context)

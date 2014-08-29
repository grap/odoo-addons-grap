# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Cooperative module for Odoo
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


class grap_member(Model):
    _description = 'Members'
    _name = 'grap.member'
    _order = "name"

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, readonly=True),
        'image': fields.binary('Image', help='Limited to 512x512px.'),
        'street': fields.char('Street', size=128),
        'zip': fields.char('Zip', size=24),
        'city': fields.char('City', size=128),
        'working_email': fields.char('Contact EMail', size=240),
        'working_phone': fields.char('Working Phone', size=64),
        'college_id': fields.many2one('grap.college', 'College'),
        'date_capital_entry': fields.date('Entry date In Capital'),
        'share_number': fields.integer('Number of Share in Capital'),
    }

    # Overload section
    def name_get(self, cr, uid, ids, context=None):
        return super(grap_member, self).name_get(cr, uid, ids, context=context)

    def name_search(
            self, cr, uid, name='', args=None, operator='ilike',
            context=None, limit=100):
        return super(grap_member, self).name_search(
            cr, uid, name=name, args=args, operator=operator,
            context=context, limit=limit)

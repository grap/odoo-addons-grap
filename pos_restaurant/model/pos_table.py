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


class pos_table(Model):
    _description = 'Restaurant table'
    _name = 'pos.table'
    _order = 'name'

    # Columns section
    _columns = {
        'name': fields.char('Name', required=True, size=64),
        'image': fields.binary('Image'),
        'active': fields.boolean(
            'Active',
            help="""By unchecking the active field you can disable """
            """a table without deleting it."""),
        'shop_id': fields.many2one(
            'sale.shop', 'Shop', help="Select the shop", required=True,),
        'company_id': fields.related(
            'shop_id', 'company_id', type='many2one', relation='res.company',
            string='Company', store=True, readonly=True, required=False),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
        ('name_shop_uniq', 'unique(name,shop_id)',
            'Table name must be unique by shop!'),
    ]

    # Overload section
    def copy(self, cr, uid, id, default={}, context=None):
        table = self.read(cr, uid, id, ['name'], context=context)
        data = {'name': '%s (copy)' % (table['name'])}
        data.update(default)
        return super(pos_table, self).copy(cr, uid, id, data, context=context)

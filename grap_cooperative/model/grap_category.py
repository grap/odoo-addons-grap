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


class grap_category(Model):
    _description = 'Category of activities'
    _name = 'grap.category'

    # Field Function section
    def _get_activity_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for category in self.browse(cr, uid, ids, context):
            res[category.id] = len(category.activity_ids)
        return res

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'activity_ids': fields.many2many(
            'grap.activity', 'grap_activity_category_rel',
            'category_id', 'activity_id', 'Activities'),
        'activity_count': fields.function(
            _get_activity_count, type='integer', string='Activities count'),
    }

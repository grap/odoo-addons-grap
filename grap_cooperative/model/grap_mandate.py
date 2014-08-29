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


class grap_mandate(Model):
    _description = 'Mandate'
    _name = 'grap.mandate'

    # Columns section
    def _get_people_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for mandate in self.browse(cr, uid, ids, context):
            res[mandate.id] = len(mandate.people_ids)
        return res

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'people_ids': fields.many2many(
            'grap.people', 'grap_people_mandate_rel',
            'mandate_id', 'people_id', 'Members'),
        'people_count': fields.function(
            _get_people_count, type='integer', string='People count')
    }

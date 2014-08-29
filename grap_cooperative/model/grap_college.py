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


class grap_college(Model):
    _description = 'Colleges'
    _name = 'grap.college'

    # Field Function section
    def _get_member_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for college in self.browse(cr, uid, ids, context):
            res[college.id] = len(college.member_ids)
        return res

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'percentage': fields.integer('Percentage', required=True),
        'member_ids': fields.one2many('grap.member', 'college_id', 'Members'),
        'member_count': fields.function(
            _get_member_count, type='integer', string='Members count'),
    }

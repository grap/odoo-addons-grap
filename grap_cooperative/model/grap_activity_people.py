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
from openerp.tools.translate import _


class grap_activity_people(Model):
    _description = 'Relation between activities and people'
    _name = 'grap.activity.people'
    _order = 'people_id'
    _rec_name = 'complete_name'

    def _get_complete_name(self, cr, uid, ids, fields, args, context=None):
        res = []
        for gap in self.browse(cr, uid, ids, context=context):
            res.append((
                gap.id,
                _('%s (%s FTE)') % (gap.activity_id.name, gap.fte)))
        return dict(res)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for pc in self.browse(cr, uid, ids):
            res.append((pc.id, pc.complete_name))
        return res

    # Columns section
    _columns = {
        'activity_id': fields.many2one(
            'grap.activity', 'Activity',
            required=True, ondelete='cascade', readonly=True),
        'people_id': fields.many2one('grap.people', 'People'),
        'fte': fields.float(
            'FTE', required=True, digits=(9, 1),
            help="Full Time Equilalent"),
        'working_email': fields.related(
            'people_id', 'working_email',
            type='char', string='Contact EMail', readonly=True),
        'private_phone': fields.related(
            'people_id', 'private_phone',
            type='char', string='Private Phone', readonly=True),
        'working_phone': fields.related(
            'people_id', 'grap_member_id', 'working_phone',
            type='char', string='Working Phone', readonly=True),
        'complete_name': fields.function(
            _get_complete_name, type='char', string='Name', store=True),
    }

    # Default section
    _defaults = {
        'fte': 1,
    }

    # Constraints section
    _sql_constraints = [
        (
            'activity_people_uniq',
            'unique(activity_id, people_id)',
            'A people can work only once time in an activity!'),
    ]

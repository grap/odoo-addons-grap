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

_GRAP_ACTIVITY_STATE = [
    ('draft', 'No linked'),
    ('progress', 'project in progress'),
    ('validated', 'Validated'),
    ('working', 'Working'),
    ('obsolete', 'project exited'),
]


class grap_activity(Model):
    _description = 'Activities'
    _name = 'grap.activity'
    _inherits = {'grap.member': 'grap_member_id'}
    _order = 'activity_name'

    # fields function section
    def _get_fte(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for ga in self.browse(cr, uid, ids, context=context):
            res[ga.id] = 0
            for gap in ga.people_ids:
                res[ga.id] += gap.fte
        return res

    # Columns section
    _columns = {
        'grap_member_id': fields.many2one(
            'grap.member', 'Member', required=True, ondelete="cascade"),
        'activity_name': fields.char('Name', size=128, required=True),
        'web_site': fields.char('Web Site', size=128),
        'state': fields.selection(
            _GRAP_ACTIVITY_STATE, 'State', required=True),
        'date_validated': fields.date('Validation date by cooperative'),
        'date_in': fields.date('Date of activity begins to work'),
        'date_out': fields.date('Date of activity ends to work'),
        'type_id': fields.many2one('grap.type', 'Type'),
        'category_ids': fields.many2many(
            'grap.category', 'grap_activity_category_rel', 'activity_id',
            'category_id', 'Categories'),
        'people_ids': fields.one2many(
            'grap.activity.people', 'activity_id', 'Workers',),
        'fte': fields.function(
            _get_fte, digits=(16, 1), string='FTE',
            help="Full Time Equivalent.", store={
                'grap.activity': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['people_ids'], 10)}),
    }

    # Default section
    _defaults = {
        'state': 'draft',
    }

    # Overloads section
    def create(self, cr, uid, data, context=None):
        data['name'] = data['activity_name']
        return super(grap_activity, self).create(
            cr, uid, data, context=context)

    def write(self, cr, uid, ids, data, context=None):
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        if 'activity_name' in data.keys():
            data['name'] = data['activity_name']
        return super(grap_activity, self).write(
            cr, uid, ids, data, context=context)

    # State section
    def state_previous(self, cr, uid, ids, context=None):
        for activity in self.browse(cr, uid, ids, context=context):
            for index in range(len(_GRAP_ACTIVITY_STATE)-1):
                if activity.state == _GRAP_ACTIVITY_STATE[index+1][0]:
                    self.write(cr, uid, activity.id, {
                        'state': _GRAP_ACTIVITY_STATE[index][0]})
            return False

    def state_next(self, cr, uid, ids, context=None):
        for activity in self.browse(cr, uid, ids, context=context):
            for index in range(len(_GRAP_ACTIVITY_STATE)-1):
                if activity.state == _GRAP_ACTIVITY_STATE[index][0]:
                    self.write(cr, uid, activity.id, {
                        'state': _GRAP_ACTIVITY_STATE[index+1][0]})
            return False

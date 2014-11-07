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
import time

_GRAP_TODO_TASK_STATE = [
    ('1_draft', 'Draft'),
    ('2_qualified', 'Qualified'),
    ('3_in_progress', 'In Progress'),
    ('4_waiting_migration', 'Waiting Migration'),
    ('5_done', 'In Production'),
    ('6_canceled', 'Canceled'),
]

_GRAP_TODO_TASK_IMPORTANCE = [
    ('undefined', 'Undefined'),
    ('low', 'Low'),
    ('average', 'Average'),
    ('high', 'High'),
]


class grap_todo_task(Model):
    _description = 'Todo Task'
    _name = 'grap.todo.task'
    _order = 'state desc, name'

    # Field Function Section
    def _get_left_days(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for gtt in self.browse(cr, uid, ids, context=context):
            res[gtt.id] = gtt.total_days - gtt.made_days
        return res

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'total_days': fields.float('Total Days', digits=(9, 1), required=True),
        'made_days': fields.float('Made Days', digits=(9, 1), required=True),
        'left_days': fields.function(
            _get_left_days, type='float', string='Left Days', store=True),
        'start_date': fields.date('Start Date', required=True),
        'stop_date': fields.date('Stop date'),
        'note': fields.text('Description'),
        'internal_note': fields.text('Internal Note'),
        'state': fields.selection(
            _GRAP_TODO_TASK_STATE, 'State', required=True),
        'importance': fields.selection(
            _GRAP_TODO_TASK_IMPORTANCE, 'Importance', required=True),
        'applicant_ids': fields.many2many(
            'grap.member', 'grap_todo_task_member_rel',
            'todo_task_id', 'member_id', 'Applicants'),
        'worker_ids': fields.many2many(
            'grap.people', 'grap_todo_task_people_rel',
            'todo_task_id', 'people_id', 'Workers'),
    }

    # Default section
    _defaults = {
        'state': '1_draft',
        'importance': 'undefined',
        'total_days': 0,
        'made_days': 0,
        'start_date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    # State section
    def state_previous(self, cr, uid, ids, context=None):
        for activity in self.browse(cr, uid, ids, context=context):
            for index in range(len(_GRAP_TODO_TASK_STATE) - 1):
                if activity.state == _GRAP_TODO_TASK_STATE[index + 1][0]:
                    self.write(cr, uid, activity.id, {
                        'state': _GRAP_TODO_TASK_STATE[index][0]})
            return False

    def state_next(self, cr, uid, ids, context=None):
        for activity in self.browse(cr, uid, ids, context=context):
            for index in range(len(_GRAP_TODO_TASK_STATE) - 1):
                if activity.state == _GRAP_TODO_TASK_STATE[index][0]:
                    self.write(cr, uid, activity.id, {
                        'state': _GRAP_TODO_TASK_STATE[index + 1][0]})
            return False

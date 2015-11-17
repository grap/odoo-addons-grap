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

from datetime import datetime

from openerp.osv import fields
from openerp.osv.orm import Model


class grap_timesheet(Model):
    _description = 'Time Sheet'
    _name = 'grap.timesheet'
    _order = 'min_date, max_date, type_id'

    # Fields Function Section
    def _get_amount_activity(
            self, cr, uid, ids, pFields, args, context=None):
        res = {}
        for gt in self.browse(cr, uid, ids, context=context):
            fmt = '%Y-%m-%d %H:%M:%S'
            d1 = datetime.strptime(gt.min_date, fmt)
            d2 = datetime.strptime(gt.max_date, fmt)
            amount = (d2 - d1).seconds / 3600.0
            res[gt.id] = {
                'amount': amount,
                'activity_qty': len(gt.activity_ids),
                'amount_per_activity': amount / len(gt.activity_ids),
            }
        return res

    def _get_timesheet_group_id(
            self, cr, uid, ids, pFields, args, context=None):
        return dict([(x, False) for x in ids])

    def _set_timesheet_group_id(
            self, cr, uid, pId, field_name, field_value, args, context=None):
        pass

    # Columns section
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'user_id': fields.many2one('res.users', 'User', required=True),

        'min_date': fields.datetime(
            string='Minimum date', required=True),
        'max_date': fields.datetime(
            string='Maximum date', required=True),

        'activity_ids': fields.many2many(
            'grap.activity',
            'grap_timesheet_activity_rel', 'timesheet_id', 'activity_id',
            'Activities', required=True),
        'type_id': fields.many2one(
            'grap.timesheet.type', 'Work Type', required=True),
        'timesheet_group_id': fields.function(
            _get_timesheet_group_id, type='many2one',
            fnct_inv=_set_timesheet_group_id,
            relation='grap.timesheet.group', string='Group'),

        'amount': fields.function(
            _get_amount_activity, type='float', string='Hours',
            help='Specifies the amount of worked hours.',
            multi='activity', store={
                'grap.timesheet': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'activity_ids', 'min_date', 'max_date',
                    ], 10)}),

        'activity_qty': fields.function(
            _get_amount_activity, type='integer', string='Activities Quantity',
            multi='activity', store={
                'grap.timesheet': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'activity_ids', 'min_date', 'max_date',
                    ], 10)}),
        'amount_per_activity': fields.function(
            _get_amount_activity, type='float', string='Amount Per Activity',
            multi='activity', store={
                'grap.timesheet': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'activity_ids', 'min_date', 'max_date',
                    ], 10)}),
    }

    # Default Section
    def _get_default_min_date(self, cr, uid, context=None):
        # TODO Make now without minut
        return fields.date.context_today(self, cr, uid, context=context)

    def _get_default_max_date(self, cr, uid, context=None):
        return fields.date.context_today(self, cr, uid, context=context)

    _defaults = {
        'name': '/',
        'user_id': lambda obj, cr, uid, context: uid,
        'min_date': _get_default_min_date,
        'max_date': _get_default_max_date,
    }

    # Views section
    def on_change_timesheet_group_id(
            self, cr, uid, ids, timesheet_group_id, context=None):
        if not timesheet_group_id:
            values = {}
        else:
            gtg_obj = self.pool['grap.timesheet.group']
            gtg = gtg_obj.browse(cr, uid, timesheet_group_id, context=context)
            values = {'activity_ids': [x.id for x in gtg.activity_ids]}
        return {'value': values}

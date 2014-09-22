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

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class grap_timesheet_report(Model):
    _name = 'grap.timesheet.report'
    _auto = False
    _description = "Analysis of TimeSheet"
    _table_name = 'grap_timesheet_report'

    _columns = {
        'worker_id': fields.many2one(
            'grap.people', 'Worker', readonly=True),
        'date': fields.date(
            'Date', readonly=True),
        'week': fields.char(
            'Week', readonly=True),
        'activity_id': fields.many2one(
            'grap.activity', 'Activity', readonly=True),
        'type_id': fields.many2one(
            'grap.timesheet.type', 'Work Type', required=True),
        'amount': fields.float('Amount', readonly=True),
        'name': fields.char(
            'Name', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table_name)
        cr.execute("""
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () as id,
        gt.date,
        gt.name,
        to_char(DATE_TRUNC('week',gt.date),'YYYY/MM/DD') as week,
        gt.type_id,
        gtar.activity_id,
        gt.worker_id,
        gt.amount_per_activity as amount
    FROM grap_timesheet_activity_rel gtar
    LEFT OUTER JOIN grap_timesheet gt
        ON gt.id = gtar.timesheet_id
)""" % (self._table_name))

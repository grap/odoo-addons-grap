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


class grap_timesheet_type(Model):
    _description = 'Time Sheet type'
    _name = 'grap.timesheet.type'
    _order = 'complete_name'

    # Custom Section
    def _compute_complete_name(self, cr, uid, id, context=None):
        gtt = self.browse(cr, uid, id, context=context)
        if gtt.parent_id:
            res = self._compute_complete_name(
                cr, uid, gtt.parent_id.id, context=context) + ' / ' + gtt.name
        else:
            res = gtt.name
        return res

    # Search Section
    def name_search(
            self, cr, uid, name='', args=None, operator='ilike', context=None,
            limit=80):
        ids = []
        ids = self.search(
            cr, uid, [
                ('complete_name', operator, name)] + args,
            limit=limit, context=context)
        return self.name_get(cr, uid, ids)

    # Getter Section
    def _get_complete_name(self, cr, uid, ids, fields, args, context=None):
        res = []
        for gtt in self.browse(cr, uid, ids, context=context):
            res.append((gtt.id, self._compute_complete_name(
                cr, uid, gtt.id, context=context)))
        return dict(res)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for gtt in self.browse(cr, uid, ids):
            res.append((gtt.id, gtt.complete_name))
        return res

    # Columns section
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'active': fields.boolean('Active'),
        'parent_id': fields.many2one(
            'grap.timesheet.type', 'Parent'),
        'complete_name': fields.function(
            _get_complete_name, type='char', string='Complete Name',
            store=True),
    }

    _defaults = {
        'active': True,
    }

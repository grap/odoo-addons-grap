# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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


class sale_recovery_moment(Model):
    _description = 'Recovery Moment'
    _name = 'sale.recovery.moment'
    _order = 'min_recovery_date, place_id'

    # Field Functions Section
    def _get_duration(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        txt = '%Y-%m-%d %H:%M:%S'
        for srm in self.browse(cr, uid, ids, context):
            d1 = datetime.strptime(srm.min_recovery_date, txt)
            d2 = datetime.strptime(srm.max_recovery_date, txt)
            res[srm.id] = (d2 - d1).seconds / (60 ** 2)
        return res

    def _get_order_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            res[srm.id] = len(srm.order_ids)
        return res

    def _get_picking_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            res[srm.id] = len(srm.picking_ids)
        return res

    def _get_complete_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            address_format = srm.country_id \
                and srm.country_id.address_format \
                or "%(street)s\n%(street2)s\n%(city)s %(state_code)s" \
                " %(zip)s\n%(country_name)s"
            args = {
                'street': srm.street and srm.street or '',
                'street2': srm.street2 and srm.street2 or '',
                'zip': srm.zip and srm.zip or '',
                'city': srm.city and srm.city or '',
                'state_code': srm.state_id and srm.state_id.code or '',
                'state_name': srm.state_id and srm.state_id.name or '',
                'country_code': srm.country_id and srm.country_id.code or '',
                'country_name': srm.country_id and srm.country_id.name or '',
            }
            res[srm.id] = srm.name + ' - ' \
                + (address_format % args).replace('\n', ' ')
        return res

    # Columns Section
    _columns = {
        'name': fields.char(
            'Name', readonly=True, required=True),
        'place_id': fields.many2one(
            'sale.recovery.place', 'Place', required=True),
        'group_id': fields.many2one(
            'sale.recovery.moment.group', 'Recovery Moment Group',
            ondelete='cascade'),
        'min_recovery_date': fields.datetime(
            'Minimum date for the Recovery', required=True),
        'max_recovery_date': fields.datetime(
            'Maximum date for the Recovery', required=True),
        'duration': fields.function(
            _get_duration, type='integer', string='Duration (Hour)'),
        'description': fields.text('Description'),
        'order_ids': fields.one2many(
            'sale.order', 'moment_id', 'Sale Orders', readonly=True),
        'order_qty': fields.function(
            _get_order_qty, type='integer', string='Sale Orders Quantity'),
        'picking_ids': fields.one2many(
            'stock.picking', 'moment_id', 'Stock Picking', readonly=True),
        'picking_qty': fields.function(
            _get_picking_qty, type='integer', string='Stock Picking Quantity'),
    }

    # Defaults Section
    _defaults = {
        'name': (
            lambda obj, cr, uid, context:
                obj.pool.get('ir.sequence').get(
                    cr, uid, 'sale.recovery.moment')),
    }

    # Constraint Section
    def _check_recovery_dates(self, cr, uid, ids, context=None):
        for srm in self.browse(cr, uid, ids, context=context):
            if srm.min_recovery_date >= srm.max_recovery_date:
                return False
        return True

    _constraints = [
        (
            _check_recovery_dates,
            'Error ! The minimum date of Recovery must be before the maximum'
            ' date of Recovery.',
            ['min_recovery_date', 'max_recovery_date']),
    ]

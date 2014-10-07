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
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class sale_recovery_moment_group(Model):
    _description = 'Group of Recovery Moments'
    _name = 'sale.recovery.moment.group'
    _order = 'min_sale_date desc, name'

    _STATE_SELECTION = [
        ('futur', 'Futur'),
        ('pending_sale', 'Pending Sale'),
        ('finished_sale', 'Finished Sale'),
        ('pending_recovery', 'Pending Recovery'),
        ('finished_recovery', 'Finished Recovery')
    ]

    # Search Functions Section
    def _search_type(self, cr, uid, obj, name, arg, context=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if arg[0][1] not in ('=', 'in'):
            raise except_orm(
                _("The Operator %s is not implemented !") % (arg[0][1]),
                str(arg))
        if arg[0][1] == '=':
            lst = [arg[0][2]]
        else:
            lst = arg[0][2]
        sql_lst = []
        if 'futur' in lst:
            sql_lst.append(
                "('%s' < min_sale_date)" % (now))
        if 'pending_sale' in lst:
            sql_lst.append((
                "(min_sale_date < '%s'"
                + " AND '%s' < max_sale_date)") % (now, now))
        if 'finished_sale' in lst:
            sql_lst.append((
                "(max_sale_date < '%s'"
                + " AND '%s'<min_recovery_date)") % (now, now))
        if 'pending_recovery' in lst:
            sql_lst.append((
                "(min_recovery_date < '%s'"
                + " AND '%s' < max_recovery_date)") % (now, now))
        if 'finished_recovery' in lst:
            sql_lst.append(
                "(max_recovery_date < '%s')" % (now))

        where = sql_lst[0]
        for item in sql_lst[1:]:
            where += " OR %s" % (item)
        sql_req = """
            SELECT id
            FROM sale_recovery_moment_group
            WHERE %s;""" % (where)
        print sql_req
        cr.execute(sql_req)
        res = cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    # Field Functions Section
    def _get_date(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for srmg in self.browse(cr, uid, ids, context):
            if len(srmg.moment_ids) == 0:
                min_date = None
                max_date = None
            else:
                min_date = min([x.min_recovery_date for x in srmg.moment_ids])
                max_date = max([x.max_recovery_date for x in srmg.moment_ids])
            if now < srmg.min_sale_date:
                state = 'futur'
            elif now < srmg.max_sale_date:
                state = 'pending_sale'
            elif now < min_date:
                state = 'finished_sale'
            elif now < max_date:
                state = 'pending_recovery'
            else:
                state = 'finished_recovery'
            res[srmg.id] = {
                'state': state,
                'min_recovery_date': min_date,
                'max_recovery_date': max_date,
            }
        return res

    def _get_order(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srmg in self.browse(cr, uid, ids, context):
            order_ids = []
            order_qty = 0
            incl_total = 0.0
            excl_total = 0.0
            for srm in srmg.moment_ids:
                order_ids.extend([order.id for order in srm.order_ids])
                order_qty += len(srm.order_ids)
                for order in srm.order_ids:
                    excl_total += order.amount_untaxed
                    incl_total += order.amount_total
            res[srmg.id] = {
                'excl_total': excl_total,
                'incl_total': incl_total,
                'order_ids': order_ids,
                'order_qty': order_qty,
            }
        return res

    def _get_picking(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srmg in self.browse(cr, uid, ids, context):
            picking_ids = []
            picking_qty = 0
#            for srm in srmg.moment_ids:
#                order_ids.extend([order.id for order in srm.order_ids])
#                order_qty += len(srm.order_ids)
#                for order in srm.order_ids:
#                    excl_total += order.amount_untaxed
#                    incl_total += order.amount_total
            res[srmg.id] = {
                'picking_ids': picking_ids,
                'picking_qty': picking_qty,
            }
        return res

    # Column Section
    _columns = {
        'name': fields.char(
            'Name', readonly=True, required=True),
        'min_sale_date': fields.datetime(
            'Minimum date for the Sale', required=True),
        'max_sale_date': fields.datetime(
            'Maximum date for the Sale', required=True),
        'min_recovery_date': fields.function(
            _get_date, multi='date', type='datetime',
            string='Minimum date for the Recovery', store=True),
        'max_recovery_date': fields.function(
            _get_date, multi='date', type='datetime',
            string='Maximum date for the Recovery', store=True),
        'state': fields.function(
            _get_date, multi='date', type='selection', string='State',
            fnct_search=_search_type,
            selection=_STATE_SELECTION),
        'moment_ids': fields.one2many(
            'sale.recovery.moment', 'group_id', 'Recovery Moments'),
        'shop_id': fields.many2one(
            'sale.shop', string='Shop', required=True,
            domain="[('company_id', '=', company_id)]",
            states={'futur': [('readonly', False)]}, readonly=True),
        'company_id': fields.many2one(
            'res.company', string='Company', required=True,
            states={'futur': [('readonly', False)]}, readonly=True),
        'order_ids': fields.function(
            _get_order, multi='order', type='one2many', relation='sale.order',
            string='Sale Orders', readonly=True),
        'order_qty': fields.function(
            _get_order, multi='order', type='integer',
            string='Sale Orders Quantity'),
        'picking_ids': fields.function(
            _get_picking, multi='picking', type='one2many',
            relation='stock.picking', string='Stock Picking', readonly=True),
        'picking_qty': fields.function(
            _get_picking, multi='picking', type='integer',
            string='Stock Picking Quantity'),
        'excl_total': fields.function(
            _get_order, multi='order', type='float',
            string='Total (VAT Exclude)'),
        'incl_total': fields.function(
            _get_order, multi='order', type='float',
            string='Total (VAT Include)'),
    }

    # Default Section
    def _default_shop_id(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(
            cr, uid, context=context)
        shop_ids = self.pool.get('sale.shop').search(
            cr, uid, [('company_id', '=', company_id)], context=context)
        if not shop_ids:
            return False
        return shop_ids[0]

    _defaults = {
        'name': (
            lambda obj, cr, uid, context:
                obj.pool.get('ir.sequence').get(
                    cr, uid, 'sale.recovery.moment.group')),
        'shop_id': _default_shop_id,
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
    }

    # Constraint Section
    def _check_shop_company(self, cr, uid, ids, context=None):
        for srmg in self.browse(cr, uid, ids, context=context):
            if srmg.shop_id.company_id.id != srmg.company_id.id:
                return False
        return True

    def _check_sale_dates(self, cr, uid, ids, context=None):
        for srmg in self.browse(cr, uid, ids, context=context):
            if srmg.min_sale_date >= srmg.max_sale_date:
                return False
        return True

    _constraints = [
        (
            _check_shop_company,
            'Error ! You have to select a shop that belong to the company.',
            ['shop_id', 'company_id']),
        (
            _check_sale_dates,
            'Error ! The minimum date of Sale must be before the maximum'
            ' date of Sale.',
            ['min_sale_date', 'max_sale_date']),
    ]

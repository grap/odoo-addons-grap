# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Move - Date and Ceriod Conform Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class fix_account_move_period_wizard(TransientModel):
    _name = 'fix.account.move.period.wizard'
    _description = 'Fix account move Period'

    # Overloading section
    def default_get(self, cr, uid, fields, context):
        am_obj = self.pool.get('account.move')
        ap_obj = self.pool.get('account.period')
        line_ids = []

        res = super(fix_account_move_period_wizard, self).default_get(
            cr, uid, fields, context=context)
        # get account move with incorrect period
        sql_req = """
            SELECT am.id from account_move am
            INNER JOIN account_period ap ON am.period_id = ap.id
            WHERE (am.date > ap.date_stop OR am.date < ap.date_start)
            AND ap.id = %s """ % (context.get('active_id'),)
        cr.execute(sql_req)
        am_ids = map(lambda x: x[0], cr.fetchall())

        # parse list and propose correction with new valid period
        for am in am_obj.browse(cr, uid, am_ids, context=context):
            ap_id = am_obj._get_period_from_date_company_id(
                cr, uid, am.date, am.company_id.id, context=context)
            new_period = ap_obj.browse(cr, uid, ap_id, context=context)
            line_ids.append((0, 0, {
                'account_move_id': am.id,
                'company_id': am.company_id.id,
                'date': am.date,
                'old_period_id': am.period_id.id,
                'old_fiscalyear_id': am.period_id.fiscalyear_id.id,
                'new_period_id': new_period.id,
                'new_fiscalyear_id': new_period.fiscalyear_id.id,
            }))
            res.update({'line_ids': line_ids})
        return res

    # Columns
    _columns = {
        'line_ids': fields.one2many(
            'fix.account.move.period.line.wizard', 'wizard_id',
            'Account Moves list'),
    }

    # Action section
    def apply_period_change(self, cr, uid, ids, context=None):
        am_obj = self.pool.get('account.move')
        for fampw in self.browse(cr, uid, ids, context=context):
            move_ids = [x.account_move_id.id for x in fampw.line_ids]
            am_obj.button_cancel(cr, uid, move_ids, context=context)
            for line in fampw.line_ids:
                am_obj.write(cr, uid, [line.account_move_id.id], {
                    'period_id': line.new_period_id.id,
                }, context=context)
            am_obj.button_validate(cr, uid, move_ids, context=context)
        return {}


class fix_account_move_period_line_wizard(TransientModel):
    _name = 'fix.account.move.period.line.wizard'
    _description = 'Information about an account move to fix'

    # Columns section
    _columns = {
        'wizard_id': fields.many2one(
            'fix.account.move.period.wizard', 'Wizard Reference', select=True),
        'account_move_id': fields.many2one(
            'account.move', 'Account Move to fix', readonly=True),
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'date': fields.date(
            'Move Date', readonly=True),
        'old_period_id': fields.many2one(
            'account.period', 'Old Period', readonly=True),
        'old_fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Old Fiscal Year', readonly=True),
        'new_period_id': fields.many2one(
            'account.period', 'New Period', required=True),
        'new_fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'New Fiscal Year', required=True),
    }

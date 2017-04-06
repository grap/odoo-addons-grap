# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>)
#    Some modification has been realized by GRAP:
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


import time

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.addons import decimal_precision as dp


class pos_session(Model):
    _inherit = 'pos.session'

    def _get_cash_control(self, cr, uid, ids, fieldnames, args, context=None):
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id] = True
            for ccl in record.cash_controls_list:
                if ccl.journal_id.cash_control:
                    result[record.id] = True
                    break
        return result

    def _compute_balances(self, cr, uid, ids, fieldnames, args, context=None):
        result = {}
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id] = {
                'cash_register_balance_end_real': '0.0',
                'cash_register_balance_start': '0.0',
                'cash_register_total_entry_encoding': '0.0',
                'cash_register_balance_end': '0.0',
                'cash_register_difference': '0.0',
            }
            balance_start = 0
            balance_end_real = 0
            total_entry_encoding = 0
            balance_end = 0
            difference = 0
            for ccl in record.cash_controls_list:
                if ccl.cash_register_id:
                    balance_end_real += ccl.cash_register_id.balance_end_real
                    balance_start += ccl.cash_register_id.balance_start
                    total_entry_encoding += \
                        ccl.cash_register_id.total_entry_encoding
                    balance_end += ccl.cash_register_id.balance_end
                    difference += ccl.cash_register_id.difference
            result[record.id]['cash_register_balance_start'] = balance_start
            result[record.id]['cash_register_balance_end_real'] = \
                balance_end_real
            result[record.id]['cash_register_total_entry_encoding'] = \
                total_entry_encoding
            result[record.id]['cash_register_balance_end'] = balance_end
            result[record.id]['cash_register_difference'] = difference
        return result

    def _cash_compute(self, cr, uid, ids, fieldnames, args, context=None):
        result = {}

        for record in self.browse(cr, uid, ids, context=context):
            result[record.id] = {
                'cash_journal_id': False,
                'cash_register_id': False,
            }
            for st in record.statement_ids:
                if st.journal_id.cash_control is True \
                        and st.journal_id.type == 'cash':
                    result[record.id]['cash_journal_id'] = st.journal_id.id
                    result[record.id]['cash_register_id'] = st.id
        return result

    _columns = {
        'cash_control': fields.function(
            _get_cash_control, type='boolean', string='Has Cash Control'),
        'cash_controls_list': fields.one2many(
            'pos.cash.controls', 'pos_session_id', 'Control List'),
        'cash_register_balance_end_real': fields.function(
            _compute_balances, multi='balance', type='float',
            digits_compute=dp.get_precision('Account'),
            string='Ending Balance', readonly=True,
            help="Computed using the cash control lines"),
        'cash_register_balance_start': fields.function(
            _compute_balances, multi='balance', type='float',
            digits_compute=dp.get_precision('Account'),
            string='Starting Balance',
            help="Computed using the cash control at the opening.",
            readonly=True),
        'cash_register_total_entry_encoding': fields.function(
            _compute_balances, multi='balance',
            string='Total Cash Transaction', readonly=True),
        'cash_register_balance_end': fields.function(
            _compute_balances, multi='balance', type='float',
            digits_compute=dp.get_precision('Account'),
            string='Computed Balance', readonly=True,
            help="Computed with the initial cash control and the"
            " sum of all payments.",),
        'cash_register_difference': fields.function(
            _compute_balances, multi='balance', type='float',
            string='Difference', readonly=True,
            help="Difference between the counted cash control at the"
            " closing and the computed balance."),
        'statement_ids': fields.one2many(
            'account.bank.statement', 'pos_session_id', 'Bank Statement'),
        'cash_journal_id': fields.function(
            _cash_compute, multi='cash', type='many2one',
            relation='account.journal', string='Cash Journal', store=True),
        'cash_register_id': fields.function(
            _cash_compute, multi='cash', type='many2one', store=True,
            relation='account.bank.statement', string='Cash Register'),
    }

    def _check_unicity(self, cr, uid, ids, context=None):
        for ps in self.browse(cr, uid, ids, context=None):
            # open if there is no session in 'opening_control',
            # 'opened', 'closing_control' for one user
            domain = [
                ('state', '=', 'opened'),
                ('user_id', '=', ps.user_id.id)
            ]
            count = self.search_count(cr, uid, domain, context=context)
            if count > 1:
                return False
        return True

    def _check_pos_config(self, cr, uid, ids, context=None):
        for ps in self.browse(cr, uid, ids, context=None):
            domain = [
                ('state', '=', 'opened'),
                ('config_id', '=', ps.config_id.id)
            ]
            count = self.search_count(cr, uid, domain, context=context)
            if count > 1:
                return False
        return True

    _constraints = [
        (
            _check_unicity,
            "You cannot create two active sessions with the same responsible!",
            ['user_id', 'state']),
        (
            _check_pos_config,
            "You cannot create two active sessions related to the same"
            " point of sale!", ['config_id']),
    ]

    def create(self, cr, uid, values, context=None):
        pos_session_id = super(pos_session, self).create(
            cr, uid, values, context=context)
        bank_statement_ids = self.browse(
            cr, uid, pos_session_id, context=context).statement_ids

        for st in bank_statement_ids:
            control_values = {
                'pos_session_id': pos_session_id,
                'journal_id': st.journal_id.id,
                'cash_register_id': st.id}
            self.pool['pos.cash.controls'].create(
                cr, uid, control_values, context=context)
        return pos_session_id

    def wkf_action_closing_control(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            for statement in session.statement_ids:
                if (not statement.journal_id.cash_control) and \
                        (statement.balance_end != statement.balance_end_real):
                    self.pool['account.bank.statement'].write(
                        cr, uid, [statement.id], {
                            'balance_end_real': statement.balance_end})
        return self.write(
            cr, uid, ids, {
                'state': 'closing_control',
                'stop_at': time.strftime('%Y-%m-%d %H:%M:%S')},
            context=context)

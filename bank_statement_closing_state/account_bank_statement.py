# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Bank Statement Closing State for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


from openerp.osv.orm import Model
from openerp.osv import fields


class account_bank_statement(Model):
    _inherit = 'account.bank.statement'

    def _get_statement(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.bank.statement.line').browse(
                cr, uid, ids, context=context):
            result[line.statement_id.id] = True
        return result.keys()

    def _end_balance(self, cursor, user, ids, name, attr, context=None):
        res_currency_obj = self.pool.get('res.currency')
        res_users_obj = self.pool.get('res.users')
        res = {}

        company_currency_id = res_users_obj.browse(
            cursor, user, user, context=context).company_id.currency_id.id

        statements = self.browse(cursor, user, ids, context=context)
        for statement in statements:
            res[statement.id] = statement.balance_start
            currency_id = statement.currency.id
            for line in statement.move_line_ids:
                if line.debit > 0:
                    if line.account_id.id == \
                            statement.journal_id.default_debit_account_id.id:
                        res[statement.id] += res_currency_obj.compute(
                            cursor, user, company_currency_id, currency_id,
                            line.debit, context=context)
                else:
                    if line.account_id.id == \
                            statement.journal_id.default_credit_account_id.id:
                        res[statement.id] -= res_currency_obj.compute(
                            cursor, user, company_currency_id, currency_id,
                            line.credit, context=context)

            if statement.state == 'closing':
                for line in statement.line_ids:
                    res[statement.id] += line.amount
        for r in res:
            res[r] = round(res[r], 2)

        res2 = super(account_bank_statement, self)._end_balance(
            cursor, user, ids, name, attr, context=context)
        for r in res2.keys():
            if res2[r] == 0:
                del res2[r]

        res.update(res2)
        return res

    _columns = {
        'state': fields.selection([
            ('draft', 'New'),
            ('open', 'Open'),  # used by cash statements
            ('closing', 'Closing'),  # used by cash statements
            ('confirm', 'Closed')],
            'State', required=True, readonly='1',
            help="""When new statement is created the state will be"""
            """ 'Draft'.\n'And after getting confirmation from the bank"""
            """ it will be in 'Confirmed' state."""),
        'balance_end': fields.function(
            _end_balance, store={
                'account.bank.statement': (
                    lambda self, cr, uid, ids, c={}:
                        ids, ['line_ids', 'move_line_ids'], 10),
                'account.bank.statement.line': (_get_statement, ['amount'], 10),
            },
            string='Computed Balance',
            help="""Balance as calculated based on Starting Balance and"""
            """ transaction lines"""),
    }

    _defaults = {
        'state': 'draft',
    }

    def statement_closing(
            self, cr, uid, ids, journal_type='bank', context=None):
        return self.write(cr, uid, ids, {'state': 'closing'}, context=context)

    def button_reopen(self, cr, uid, ids, journal_type='bank', context=None):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def check_status_condition(self, cr, uid, state, journal_type='bank'):
        return state in ('draft', 'open', 'closing')

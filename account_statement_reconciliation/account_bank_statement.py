# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Account Statement Reconciliation Module for Odoo
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


from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    _name = 'account.bank.statement'

    def _default_account_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        journal_pool = self.pool.get('account.journal')
        journal_type = context.get('journal_type', False)
        company_id = self.pool.get('res.company')._company_default_get(
            cr, uid, 'account.bank.statement', context=context)
        if journal_type:
            ids = journal_pool.search(cr, uid, [
                ('type', '=', journal_type), ('company_id', '=', company_id)])
            if ids:
                return journal_pool.browse(
                    cr, uid, ids[0], context=context
                ).default_debit_account_id.id
        return False

    def _theorical_end_balance(
            self, cursor, user, ids, name, attr, context=None):
        res_currency_obj = self.pool.get('res.currency')
        res_users_obj = self.pool.get('res.users')
        res = {}

        company_currency_id = res_users_obj.browse(
            cursor, user, user, context=context
        ).company_id.currency_id.id
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

            if statement.state in ('draft', 'open'):
                for line in statement.line_ids:
                    res[statement.id] += line.amount
        for r in res:
            res[r] = round(res[r], 2)
        return res

    def balance_check(self, cr, uid, st_id, journal_type='bank', context=None):
        st = self.browse(cr, uid, st_id, context=context)
        if not (abs(
                (st.theorical_balance_end or 0.0) -
                st.balance_end_real) < 0.0001):
            raise osv.except_osv(_('Error!'), _(
                """The statement balance is incorrect !\nThe finale balance"""
                """ (%.2f) is different than the computed one. (%.2f)""") % (
                    st.balance_end_real, st.theorical_balance_end))
        return True

    def button_confirm_bank(self, cr, uid, ids, context=None):
        super(account_bank_statement, self).button_confirm_bank(
            cr, uid, ids, context=context)
        for st in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [st.id], {
                'balance_end_real': st.theorical_balance_end,
            }, context=context)

    def onchange_journal_id(
            self, cr, uid, statement_id, journal_id, move_line_ids,
            context=None):
        result = super(account_bank_statement, self).onchange_journal_id(
            cr, uid, statement_id, journal_id, context=context)
        account_id = self.pool.get('account.journal').browse(
            cr, uid, journal_id, context=context).default_debit_account_id.id
        result['value']['account_id'] = account_id

        # move line ids will contain "[[6, False, []]]" if the list is empty
        # and "[[6, False, [id list]]]" if there are some records
        if move_line_ids[0][2]:
            warning = {
                'title': _('Configuration Error!'),
                'message': _(
                    """Keep in mind that you cannot validate the statement"""
                    """ if there are moves from different journals.""")
            }
            result.update({'warning': warning})
        return result

    _columns = {
        'account_id': fields.related(
            'journal_id', 'default_debit_account_id', type='many2one',
            relation='account.account', string='Account used in this journal',
            readonly=True, help="""used in statement reconciliation domain,"""
            """ but shouldn't be used elswhere."""),
        'theorical_balance_end': fields.function(
            _theorical_end_balance, string='Solde final calculé'),
    }

    _defaults = {
        'account_id': _default_account_id,
    }

    def _check_journals(self, cr, uid, ids, context=None):
        for st in self.browse(cr, uid, ids, context=context):
            journal_id = st.journal_id.id
            for move in st.move_line_ids:
                if move.journal_id.id != journal_id:
                    return False
        return True

    _constraints = [
        (
            _check_journals,
            """All selected moves must have the same journal as the"""
            """ statement.""", ['journal_id']),
    ]

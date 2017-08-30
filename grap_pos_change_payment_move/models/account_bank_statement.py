# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp.osv import osv
from openerp import _, api, models


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def button_confirm_cash(
            self, cr, uid, ids, context=None):
        """Rewrite function to make it call button_confirm_bank and not
        super(button_confirm_bank). (Odoo Core bad design) that disables
        possibility to inherit button_confirm_bank correctly.
        See file odoo/addons/account/account_cash_statement.py
        This function is written in old api, because of a weird call
        of the function button_confirm_, that forbid new api call."""
        statement_line_obj = self.pool.get('account.bank.statement.line')

        for obj in self.browse(cr, uid, ids, context=context):
            if obj.difference == 0.0:
                continue
            elif obj.difference < 0.0:
                account = obj.journal_id.loss_account_id
                name = _('Loss')
                if not obj.journal_id.loss_account_id:
                    raise osv.except_osv(_('Error!'), _(
                        'There is no Loss Account on the journal %s.') % (
                            obj.journal_id.name,))
            else:
                account = obj.journal_id.profit_account_id
                name = _('Profit')
                if not obj.journal_id.profit_account_id:
                    raise osv.except_osv(_('Error!'), _(
                        'There is no Profit Account on the journal %s.') % (
                            obj.journal_id.name,))

            values = {
                'statement_id': obj.id,
                'journal_id': obj.journal_id.id,
                'account_id': account.id,
                'amount': obj.difference,
                'name': name,
            }
            statement_line_obj.create(cr, uid, values, context=context)

        return self.button_confirm_bank(cr, uid, ids, context=context)

    def button_confirm_bank(
            self, cr, uid, ids, context=None):
        """
        Call normal super function for statement, except for PoS statement,
        that will call button_confirm_bank_point_of_sale() function.
        This function is written in old api, because of a weird call
        of the function button_confirm_, that forbid new api call."""
        res = []
        for statement in self.browse(cr, uid, ids, context=context):
            if statement.pos_session_id:
                res.append(self.button_confirm_bank_point_of_sale(
                    cr, uid, [statement.id], context=context))
            else:
                res.append(super(
                    AccountBankStatement, self).button_confirm_bank(
                        cr, uid, [statement.id], context=context))
        return all(res)

    @api.multi
    def button_confirm_bank_point_of_sale(self):
        """This function is called instead of button_confirm_bank() core
        function, if the statement is a statement from point of sale."""

        move_obj = self.env['account.move']
        statement_line_obj = self.env['account.bank.statement.line']

        for statement in self:
            move_ids = []
            groups = {}
            # parse the lines to group the ids according to the key fields
            for statement_line in statement.line_ids:
                pos_order = statement_line.pos_statement_id
                # We keep partner information only if
                # an invoice has been generated
                if pos_order and pos_order.state == 'invoiced':
                    partner_id = statement_line.partner_id.id
                else:
                    partner_id = False
                keys = (
                    statement_line.account_id.id,
                    partner_id,
                    pos_order._prepare_date_payment_move_point_of_sale())
                groups.setdefault(keys, [])
                groups[keys].append(statement_line.id)

            # for each group, create account_move and account_move_lines
            i = 0
            for key in groups.keys():
                i += 1
                statement_lines = statement_line_obj.browse(groups[key])
                move = statement.create_move_point_of_sale(
                    key, statement_lines, statement.name + "/" + str(i))
                move_ids.append(move.id)
                # Mark statement line as reconciled with a move
                statement_lines.write({'journal_entry_id': move.id})

            if move_ids:
                moves = move_obj.browse(move_ids)
                moves.post()

        return self.write({
            'state': 'confirm',
            'closing_date': time.strftime("%Y-%m-%d %H:%M:%S")}
        )

    @api.multi
    def create_move_point_of_sale(self, key, statement_lines, move_name):
        self.ensure_one()

        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']

        move_vals = self._prepare_move_point_of_sale(
            key, statement_lines, move_name)

        move = move_obj.create(move_vals)

        move_line_vals = self._prepare_bank_move_line_point_of_sale(
            key, statement_lines, move)
        move_line_obj.create(move_line_vals)

        move_line_vals = self._prepare_counterpart_move_line_point_of_sale(
            key, statement_lines, move)
        move_line_obj.create(move_line_vals)

        return move

    @api.multi
    def _prepare_move_point_of_sale(self, key, statement_lines, move_name):
        self.ensure_one()
        (account_id, partner_id, move_date) = key
        period_obj = self.env['account.period']
        return {
            'journal_id': self.journal_id.id,
            'partner_id': partner_id,
            'period_id': period_obj.find(dt=move_date).id,
            'date': move_date,
            'name': move_name,
            'ref': self.pos_session_id.name,
        }

    @api.multi
    def _prepare_bank_move_line_point_of_sale(
            self, key, statement_lines, move):
        self.ensure_one()
        (account_id, partner_id, move_date) = key
        amount = 0
        for statement_line in statement_lines:
            amount += statement_line.amount

        debit = ((amount < 0) and - amount) or 0.0
        credit = ((amount > 0) and amount) or 0.0

        return {
            'name': self.name,
            'date': move.date,
            'move_id': move.id,
            'account_id': account_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': self.id,
            'journal_id': self.journal_id.id,
            'period_id': move.period_id.id,
        }

    @api.multi
    def _prepare_counterpart_move_line_point_of_sale(
            self, key, statement_lines, move):
        self.ensure_one()
        (x, partner_id, move_date) = key
        amount = 0
        for statement_line in statement_lines:
            amount += statement_line.amount

        account_id = (
            (amount <= 0) and self.journal_id.default_debit_account_id.id) or\
            self.journal_id.default_credit_account_id.id
        debit = ((amount > 0) and amount) or 0.0
        credit = ((amount < 0) and - amount) or 0.0

        return {
            'name': self.name,
            'date': move.date,
            'move_id': move.id,
            'account_id': account_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': self.id,
            'journal_id': self.journal_id.id,
            'period_id': move.period_id.id,
        }

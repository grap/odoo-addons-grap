# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    # Columns Section
    is_pos_control = fields.Boolean(
        compute='_compute_is_pos_control', store=True, string='PoS Control')

    # Compute Section
    @api.multi
    @api.depends('journal_id.cash_control', 'journal_id.bank_control')
    def _compute_is_pos_control(self):
        for statement in self:
            journal = statement.journal_id
            if journal.type == 'cash':
                statement.is_pos_control = journal.cash_control
            elif journal.type == 'bank':
                statement.is_pos_control = journal.bank_control
            else:
                statement.is_pos_control = False

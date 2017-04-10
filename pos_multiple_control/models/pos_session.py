# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning


class PosSession(models.Model):
    _inherit = 'pos.session'

    # Columns Section
    control_statement_ids = fields.One2many(
        string='Statements', comodel_name='account.bank.statement',
        related='statement_ids')

    statement_ids = fields.One2many(readonly=False)

    control_register_balance_start = fields.Float(
        compute='_compute_control_register_balance_start',
        string='Opening Balances')

    control_register_total_entry_encoding = fields.Float(
        compute='_compute_control_register_total_entry_encoding',
        string='Transactions')

    control_register_balance_end = fields.Float(
        compute='_compute_control_register_balance_end',
        string='Theoretical Closing Balances')

    control_register_balance_end_real = fields.Float(
        compute='_compute_control_register_balance_end_real',
        string='Real Closing Balance')

    control_register_difference = fields.Float(
        compute='_compute_control_register_difference',
        string='Differences')

    # Compute Section
    @api.multi
    @api.depends('statement_ids.is_pos_control', 'statement_ids.balance_start')
    def _compute_control_register_balance_start(self):
        for session in self:
            session.control_register_balance_start = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control==True).mapped('balance_start'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.total_entry_encoding')
    def _compute_control_register_total_entry_encoding(self):
        for session in self:
            session.control_register_total_entry_encoding = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control==True).mapped(
                        'total_entry_encoding'))

    @api.multi
    @api.depends('statement_ids.is_pos_control', 'statement_ids.balance_end')
    def _compute_control_register_balance_end(self):
        for session in self:
            session.control_register_balance_end = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control==True).mapped('balance_end'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.balance_end_real')
    def _compute_control_register_balance_end_real(self):
        for session in self:
            session.control_register_balance_end_real = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control==True).mapped(
                        'balance_end_real'))

    @api.multi
    @api.depends('statement_ids.is_pos_control', 'statement_ids.difference')
    def _compute_control_register_difference(self):
        for session in self:
            session.control_register_difference = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control==True).mapped('difference'))

    # Overload Section
    @api.model
    def create(self, vals):
        session = super(PosSession, self).create(vals)
        session.opening_details_ids.write({'is_piece': True})
        return session

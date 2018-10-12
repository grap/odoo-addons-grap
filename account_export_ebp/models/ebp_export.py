# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class EbpExport(models.Model):
    _name = 'ebp.export'
    _order = 'date desc'

    # Column Section
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True,
        readonly=True)

    fiscalyear_id = fields.Many2one(
        comodel_name='account.fiscalyear', string='Fiscal year', required=True,
        readonly=True)

    date = fields.Datetime(
        'Date', required=True, readonly=True)

    name = fields.Char(
        compute='_compute_name', string='Name', store=True, readonly=True)

    description = fields.Text(
        string='Description', readonly=True,
        help="Extra Description for Accountant Manager.")

    exported_move_qty = fields.Integer(
        oldname='exported_moves',
        string='Quantity of Moves Exported', readonly=True)

    exported_account_qty = fields.Integer(
        oldname='exported_accounts',
        string='Quantity of accounts exported', readonly=True)

    exported_moves_ids = fields.One2many(
        comodel_name='account.move', inverse_name='ebp_export_id',
        string='Exported Moves', readonly=True)

    data_moves = fields.Binary(
        string='Moves file', readonly=True)

    data_accounts = fields.Binary(
        string='Accounts file', readonly=True)

    data_balance = fields.Binary(
        string='Balance file', readonly=True)

    file_name_moves = fields.Char(
        readonly=True, compute='_compute_file_name_moves')

    file_name_accounts = fields.Char(
        readonly=True, compute='_compute_file_name_accounts')

    file_name_balance = fields.Char(
        readonly=True, compute='_compute_file_name_balance')

    # Compute Section
    @api.multi
    def _compute_name(self):
        for export in self:
            export.name = 'export_%d' % export.id

    @api.multi
    def _compute_file_name_moves(self):
        for export in self:
            export.file_name_moves =\
                'export_%d_%s.csv' % (export.id, _("MOVES"))

    @api.multi
    def _compute_file_name_accounts(self):
        for export in self:
            export.file_name_accounts =\
                'export_%d_%s.csv' % (export.id, _("ACCOUNTS"))

    @api.multi
    def _compute_file_name_balance(self):
        for export in self:
            export.file_name_balance =\
                'export_%d_%s.csv' % (export.id, _("BALANCE"))

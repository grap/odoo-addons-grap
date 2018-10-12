# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    # Columns section
    ebp_suffix = fields.Char(
        string="Suffix in EBP", oldname="ref_nb",
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a new Account.")

    move_line_qty = fields.Integer(
        compute='_compute_move_line_qty',
        string='Quantity of Account Move Lines',
        help="Number of account moves for this partner")

    @api.multi
    def _compute_move_line_qty(self):
        pass
        # AccountMoveLine = self.env['account.move.line']

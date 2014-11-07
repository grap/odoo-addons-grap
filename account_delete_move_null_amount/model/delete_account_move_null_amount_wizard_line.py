# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Delete Null Account Move Module for Odoo
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


class delete_account_move_null_amount_wizard_line(TransientModel):
    _name = 'delete.account.move.null.amount.wizard.line'
    _description = "Information about an account move to delete"

    # Columns section
    _columns = {
        'wizard_id': fields.many2one(
            'delete.account.move.null.amount.wizard', 'Wizard Reference',
            select=True),
        'account_move_id': fields.many2one(
            'account.move', 'Account Move to delete', readonly=True),
        'period_id': fields.many2one(
            'account.period', 'Period', readonly=True),
        'journal_id': fields.many2one(
            'account.journal', 'Journal', readonly=True),
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'date': fields.date(
            'Move Date', readonly=True),
    }

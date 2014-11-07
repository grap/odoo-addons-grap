# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Invoice 'Verified' state Module for Odoo
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
from openerp.osv import osv
from openerp.tools.translate import _


class account_invoice(Model):
    _inherit = 'account.invoice'

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft'),
            ('verified', 'Verified'),
            ('proforma', 'Pro-forma'),
            ('proforma2', 'Pro-forma'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled')
        ], 'State', select=True, readonly=True,
            help="""* The 'Draft' state is used when a user is encoding"""
            """ a new and unconfirmed Invoice."""
            """\n* The 'Pro-forma' when invoice is in Pro-forma state,"""
            """ invoice does not have an invoice number."""
            """\n* The 'Verified' state is used when the user has checked"""
            """ that the invoice is conform to what he expected and is"""
            """ ready to be processed by the accountants."""
            """\n* The 'Open' state is used when user create invoice,"""
            """ a invoice number is generated.Its in open state till user"""
            """ does not pay invoice."""
            """\n* The 'Paid' state is set automatically when the invoice"""
            """ is paid. Its related journal entries may or may not be"""
            """ reconciled."""
            """\n* The 'Cancelled' state is used when user cancel invoice."""),
    }

    def wkf_verify_invoice(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context=context):
            if not invoice.date_invoice or not invoice.date_due:
                raise osv.except_osv(_('Error!'), _(
                    """Verify a supplier invoice requires to set"""
                    """ 'invoice date' and 'due date' fields."""))
        self.write(cr, uid, ids, {'state': 'verified'})
        return True

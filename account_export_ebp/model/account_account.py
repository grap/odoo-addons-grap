# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

from openerp.osv import fields
from openerp.osv.orm import Model


class account_account(Model):
    _inherit = 'account.account'

    # Columns section
    _columns = {
        'code': fields.char('Code', size=10, required=True, select=1),
        'export_tax_code': fields.boolean(
            'Export according to Tax Codes',
            help="""If checked, when you export moves from this account,"""
            """ it will create one account for each Tax Code"""),
        'ebp_code_no_tax': fields.char(
            'Tax Code\'s Account suffix in EBP (if no tax)', size=4,
            help="When exporting Entries to EBP, this suffix will be"
            " appended to the Account Number to make it a new Account,"
            " if Export according to tax Codes is checked, and"
            " if no taxes is defined on the account move line."),
    }

    # Defaults section
    _defaults = {
        'export_tax_code': False,
    }

    # Constraints section
    def _check_code_length(self, cr, uid, ids, context=None):
        for account in self.browse(cr, uid, ids, context=context):
            if account.company_id.fiscal_type == 'fiscal_mother':
                if account.is_intercompany_trade_fiscal_company and\
                        len(account.code) > 6:
                    return False
                elif not account.is_intercompany_trade_fiscal_company and\
                        account.type in ('receivable', 'payable') and\
                        len(account.code) > 3:
                    return False
            elif account.company_id.fiscal_type == 'normal':
                if account.type in ('receivable', 'payable') and\
                        len(account.code) > 6:
                    return False
        return True

    _constraints = [
        (
            _check_code_length,
            "The account code for a partner account cannot exceed\n"
            " * 3 characters for Fiscal Mother Company (Regular Case);\n"
            " * 6 characters for Fiscal Mother Company (Intercompany Trade);\n"
            " * 6 characters for Normal Company ; \n"
            " so as to permit the EBP export",
            ['code', 'type', 'company_id',
                'is_intercompany_trade_fiscal_company']),
    ]

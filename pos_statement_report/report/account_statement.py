# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from point_of_sale.report import account_statement
from report import report_sxw


class account_statement(account_statement.account_statement):

    def __init__(self, cr, uid, name, context):
        super(account_statement, self).__init__(cr, uid, name, context=context)
        self.get_nb_lines = 0
        self.localcontext.update({
            'get_nb_lines': self._get_nb_lines,
        })

    def _get_nb_lines(self, statement_line_ids):
        return len(statement_line_ids) or 0

# remove previous sale.report service :
from netsvc import Service
del Service._services['report.account.statement']

# register the new report service :
report_sxw.report_sxw(
    'report.account.statement',
    'account.bank.statement',
    'addons/pos_statement_report/report/account_statement.rml',
    parser=account_statement,
    header='internal',
    )

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>)
#    Some modification has been realized by GRAP:
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


from openerp.osv.orm import Model


class account_cash_statement(Model):
    _inherit = 'account.bank.statement'

    def _update_balances_no_cash(self, cr, uid, ids, context=None):
        """
            Set starting and ending balances according to pieces count
        """
        res = {}
        for acs in self.browse(cr, uid, ids, context=context):
            if ((
                acs.journal_id.type in ('cash',))
                    or (not acs.journal_id.cash_control)):
                continue
            start = end = 0
            for line in acs.details_ids:
                start += line.subtotal_opening
                end += line.subtotal_closing
            data = {
                'balance_start': start,
                'balance_end_real': end,
            }
            res[acs.id] = data
            super(account_cash_statement, self).write(
                cr, uid, [acs.id], data, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(account_cash_statement, self).write(
            cr, uid, ids, vals, context=context)
        self._update_balances_no_cash(cr, uid, ids, context)
        return res

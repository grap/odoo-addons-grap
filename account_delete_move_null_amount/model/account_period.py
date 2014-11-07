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

from openerp.osv import fields
from openerp.osv.orm import Model


class account_period(Model):
    _inherit = 'account.period'

    # Field function section
    def _get_account_move_null_amount_quantity(
            self, cr, uid, ids, name, arg, context=None):
        """Return the number of account moves with null amount"""
        res = {}
        for id in ids:
            res[id] = 0
        cr.execute("""
            SELECT period_id, count(*)
            FROM(
                SELECT period_id, move_id
                FROM account_move_line
                WHERE period_id in %s
                GROUP BY move_id, period_id
                HAVING SUM(debit) = 0 AND SUM(credit) = 0
            ) temp
            GROUP BY period_id""", (tuple(ids),))
        for item in cr.fetchall():
            res[item[0]] = item[1]
        return res

    # Columns section
    _columns = {
        'account_move_null_amount_quantity': fields.function(
            _get_account_move_null_amount_quantity, type='integer',
            string='Quantity of moves with null amount'),
    }

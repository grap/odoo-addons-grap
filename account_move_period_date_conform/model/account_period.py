# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Move - Date and Ceriod Conform Module for Odoo
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
    def _get_account_move_incorrect_date_quantity(
            self, cr, uid, ids, name, arg, context=None):
        """Return the number of account moves with incorrect dates"""
        res = {x: 0 for x in ids}
        sql_req = """
            SELECT ap.id, count(*) from account_move am
            INNER JOIN account_period ap on am.period_id = ap.id
            WHERE am.date > ap.date_stop or am.date < ap.date_start
            and ap.id in (%s)
            GROUP BY ap.id""" % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall():
            res[item[0]] = item[1]
        return res

    # Columns section
    _columns = {
        'account_move_incorrect_date_quantity': fields.function(
            _get_account_move_incorrect_date_quantity, type='integer',
            string='Quantity of moves with incorrect period'),
    }

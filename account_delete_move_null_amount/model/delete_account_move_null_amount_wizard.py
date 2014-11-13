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


class delete_account_move_null_amount_wizard(TransientModel):
    _name = 'delete.account.move.null.amount.wizard'

    # Overloading section
    def default_get(self, cr, uid, pFields, context):
        am_obj = self.pool.get('account.move')
        line_ids = []

        res = super(delete_account_move_null_amount_wizard, self).default_get(
            cr, uid, pFields, context=context)
        # get account move with null amount
        cr.execute("""
                SELECT move_id
                FROM account_move_line
                WHERE period_id = %s
                GROUP BY move_id
                HAVING SUM(debit) = 0 AND SUM(credit) = 0
            """, (context.get('active_id'),))

        am_ids = map(lambda x: x[0], cr.fetchall())

        # parse list and propose correction with new valid period
        for am in am_obj.browse(cr, uid, am_ids, context=context):
            line_ids.append((0, 0, {
                'account_move_id': am.id,
                'company_id': am.company_id.id,
                'date': am.date,
                'period_id': am.period_id.id,
                'journal_id': am.journal_id.id,
            }))
            res.update({'line_ids': line_ids})
        return res

    # Columns
    _columns = {
        'line_ids': fields.one2many(
            'delete.account.move.null.amount.wizard.line', 'wizard_id',
            'Account Moves list'),
    }

    # Action section
    def delete_account_move(self, cr, uid, ids, context=None):
        am_obj = self.pool.get('account.move')
        for damnaw in self.browse(cr, uid, ids, context=context):
            move_ids = [x.account_move_id.id for x in damnaw.line_ids]
            am_obj.button_cancel(cr, uid, move_ids, context=context)
            am_obj.unlink(cr, uid, move_ids, context=context)
        return {}

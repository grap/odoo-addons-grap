# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Mass Drop Moves Module for Odoo
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

import logging
from openerp.osv import fields
from openerp.osv.orm import TransientModel

_logger = logging.getLogger(__name__)


class account_mass_drop_moves_wizard(TransientModel):
    _name = 'account.mass.drop.moves.wizard'

    # Constants section
    MAX_RECORDS = 500

    # Columns
    _columns = {
        'journal_id': fields.many2one(
            'account.journal', 'Journal', required=True),
        'period_id': fields.many2one(
            'account.period', 'Period', required=True),
        'move_qty': fields.integer(
            'Moves Quantity to delete', readonly=True),
    }

    # Views section
    def on_change_journal_period(
            self, cr, uid, ids, journal_id, period_id, context=None):
        if not (journal_id and period_id):
            values = {'move_qty': 0}
        else:
            am_obj = self.pool['account.move']
            am_ids = am_obj.search(cr, uid, [
                ('journal_id', '=', journal_id), ('period_id', '=', period_id),
            ], context=context)
            values = {'move_qty': len(am_ids)}
        return {'value': values}

    # Action section
    def drop_account_moves(self, cr, uid, ids, context=None):
        am_obj = self.pool['account.move']
        for amdmw in self.browse(cr, uid, ids, context=context):
            all_am_ids = am_obj.search(cr, uid, [
                ('journal_id', '=', amdmw.journal_id.id),
                ('period_id', '=', amdmw.period_id.id),
            ], context=context)
            for i in range(0, len(all_am_ids), self.MAX_RECORDS):
                am_ids = all_am_ids[i:i + self.MAX_RECORDS]
                _logger.info(
                    "Cancel %d Account Moves in %s for the period %s" % (
                        len(am_ids), amdmw.journal_id.name,
                        amdmw.period_id.name))
                am_obj.button_cancel(cr, uid, am_ids, context=context)
                _logger.info(
                    "Unlink %d Account Moves in %s for the period %s" % (
                        len(am_ids), amdmw.journal_id.name,
                        amdmw.period_id.name))
                am_obj.unlink(cr, uid, am_ids, context=context)
        return {}

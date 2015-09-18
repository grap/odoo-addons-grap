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


class account_move(Model):
    _inherit = 'account.move'

    def create(self, cr, uid, vals, context=None):
        aj_obj = self.pool['account.journal']
        if vals.get('journal_id', False) and not vals.get('to_check'):
            aj = aj_obj.browse(cr, uid, vals['journal_id'], context=context)
            vals['to_check'] = aj.move_to_check
        return super(account_move, self).create(cr, uid, vals, context=context)

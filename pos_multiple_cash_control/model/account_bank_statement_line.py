# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp.osv.osv import except_osv
from openerp.osv.orm import Model
from openerp.tools.translate import _

class account_bank_statement_line(Model):
    _inherit = 'account.bank.statement.line'

    def unlink(self, cr, uid, ids, context=None):
        for absl in self.browse(cr, uid, ids, context=context):
            if absl.pos_statement_id and\
                    absl.pos_statement_id.state != 'draft':
                raise except_osv(
                    _('Error!'),
                    _("Unable to delete a payment of a Pos Order that is"
                    " not in a draft state!"))
        res = super(account_bank_statement_line, self).unlink(
            cr, uid, ids, context=context)
        return res


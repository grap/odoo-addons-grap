# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Move Change Number Module for Odoo
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

from openerp.osv.orm import Model
from openerp.tools.translate import _


class account_move(Model):
    _inherit = 'account.move'

    def rename_account_move_change_number(self, cr, uid, ids, context=None):
        for id in ids:
            old_account_move = self.browse(cr, uid, id, context=context)
            old_name = old_account_move.name
            old_narration = old_account_move.narration or ''
            # unpost acount move
            self.button_cancel(cr, uid, [id], context=context)

            # set name to "/"
            self.write(cr, uid, [id], {'name': '/'}, context=context)

            # post account move
            self.post(cr, uid, [id], context=context)
            new_name = self.browse(cr, uid, id, context=context).name

            # Add description of the change
            self.write(cr, uid, [id], {
                'narration': old_narration + _(
                    """\nAccount move renamed old name : %s ;"""
                    """ new name : %s""") % (old_name, new_name)
            }, context=context)
        return True

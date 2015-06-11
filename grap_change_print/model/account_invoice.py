# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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
from openerp.osv import fields


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    # Columns section
    def _get_has_discount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for ai in self.browse(cr, uid, ids, context=context):
            res[ai.id] = any([line.discount for line in ai.invoice_line])
        return res

    _columns = {
        'has_discount': fields.function(
            _get_has_discount, type='boolean',
            string='Indicate that there is some discount in Invoice Lines'),
    }

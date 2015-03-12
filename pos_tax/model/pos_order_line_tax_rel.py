# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Tax Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

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


class pos_order_line_tax_rel(Model):
    _name = 'pos.order.line.tax.rel'

    # Columns section
    _columns = {
        'tax_id': fields.many2one(
            'account.tax', 'Tax', required=True),
        'orderline_id': fields.many2one(
            'pos.order.line', 'Order Line', required=True, ondelete='cascade'),
        'baseHT': fields.float(
            'Base HT'),
        'amount_tax': fields.float(
            'Tax Amount'),
    }

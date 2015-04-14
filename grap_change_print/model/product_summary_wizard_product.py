# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print Module for Odoo
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class ProductSummaryWizardProduct(TransientModel):
    _name = 'product.summary.wizard.product'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'product.summary.wizard', 'Wizard', select=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True, readonly=True),
        'quantity': fields.float(
            'Quantity', required=True, readonly=True),
        'uom_id': fields.many2one(
            'product.uom', 'UoM', required=True, readonly=True),
        'standard_price': fields.float(
            'Standard Price', required=True, readonly=True),
        'standard_price_total': fields.float(
            'Standard Price Total', required=True, readonly=True),
    }

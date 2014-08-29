# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Taxes Required module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


class product_product(Model):
    _inherit = 'product.product'

    # Constraints Section
    def _check_sale_tax_required(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            if product.sale_ok and len(product.taxes_id) == 0:
                return False
        return True

    def _check_purchase_tax_required(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            if (product.purchase_ok) and len(product.supplier_taxes_id) == 0:
                return False
        return True

    _constraints = [
        (
            _check_sale_tax_required,
            'Error: You must define a sale tax if the product can be sold.',
            ['sale_ok', 'taxes_id']),
        (
            _check_purchase_tax_required,
            """Error: You must define a purchase tax if the product can be"""
            """ purchased.""",
            ['purchase_ok', 'supplier_taxes_id']),
    ]

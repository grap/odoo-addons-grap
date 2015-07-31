# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Precision module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

{
    'name': 'GRAP - Change Precision',
    'version': '0.1',
    'summary': 'Change the precisions names and values of some fields',
    'category': 'Tools',
    'description': """
Change the precisions names and values of some fields
=====================================================

Functionality:
--------------
    * Add a new precision 'GRAP Purchase Unit Price', used in:
        * stock_move.unit_price;
        * account_invoice_line.price_unit;
        * purchase_order_line.price_unit;
        * product_template.standard_price;

# NO -> FIXME in V8, with real API that allow to change precision,
# without rewriting all the wheel;
        * product_template.standard_price_vat_included;
    * Add a new precision 'GRAP Purchase Unit Discount', used in:
        * account_invoice_line.discount;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'account',
        'purchase',
        'point_of_sale',
        'product_standard_price_vat_incl',
    ],
    'data': [
        'data/decimal_precision.xml',
    ],
}

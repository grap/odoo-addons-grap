# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Translation module for Odoo
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

{
    'name': 'GRAP - Change translation',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Disable the mechanism of translation for the following field:
=============================================================

* **account_payment_term**: name;
* **account_tax**: name;
* **pos_category**: name;
* **product_category**: name;
* **product_pricelist**: name;
* **product_template**: name, description, description_purchase,"""
    """ description_sale;
* **product_ul**: name ;
* **product_uom**: name ;
* **res_partner_category**: name;
* **stock_location**: name;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author : Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'product',
        'stock',
        'point_of_sale',
    ],
}

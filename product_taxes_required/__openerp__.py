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


{
    'name': 'Product - Taxes Required',
    'version': '2.1',
    'category': 'Sales',
    'description': """
Add restriction during creation & modification of a product.
============================================================

Features :
----------
    * Forbid to save a **sale_ok** product if no sale taxes are defined ;
    * Forbid to save a **purchase_ok** product if no purchase taxes are"""
    """ defined;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'product',
        'purchase',
    ],
    'data': [
        'view/product_view.xml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Improved Search Module for Odoo
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
{
    'name': 'Product - Improved Search',
    'version': '2.1',
    'category': 'Product',
    'description': """
-> This module slighly changes the product search function to allow multi words
search, usefull when you have a lot of products.
It uses the ":" as a separator. The order of the words you type doesn't matter.
For example, if you search "rice:ital:whit", it will find a product named
"white rice from italia 1kg"

When you install this module, all product names containing the separator will
be changed.
By default, the ':' in product names will be replaced by ''.
Those values can be changed in the model/product.py, with the _SEPARATOR and
_REPLACEMENT constants.

-> This module also provides unaccent search against the products. To activate
this, you have to:
- install postgresql-contrib package (sudo apt-get install postgresql-contrib)
- run this request as a superuser on the db you use:
        CREATE EXTENSION unaccent;
- restart your OE server with --unaccent option

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'init/init.xml',
    ],
}

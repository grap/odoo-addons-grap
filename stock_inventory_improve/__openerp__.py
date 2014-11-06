# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Inventory Improve Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
    'name': 'Stock - Inventory Improve',
    'version': '2.0',
    'category': 'Stock',
    'description': """
Improve Inventory
=================

Functionnality:
---------------
    * Display a better message in case of uom problems, mentionning
      the product;
    * Add an option to reset the stock account when you fill the inventory
      with 0;
    * Improve stock location selection when you fill the inventory;
    * Fix a bug on fill_inventory. price_unit is lost;
    * Add a button fill price_unit to set price_unit correctly on draft
      inventory;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2013, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'stock',
        'stock_inventory_valuation',
    ],
    'data': [
        'view/view.xml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Inventory - Sum Duplicates for Odoo
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
    'name': 'Stock Inventory - Sum Duplicates',
    'version': '1.1',
    'category': 'Stock',
    'description': """
Feature:
--------
    * If a stock.inventory has several lines with same product, lot and
      location, the lines will be merged and the quantities will be summed
      before creating the stock.moves;

Use Case:
---------
    * This module is usefull when the product is in many location that are
      not defined in OpenERP. For example, in a little shop, a product can be:
        * in stock; (in one or many places);
        * in the sales area; (in one or many places);

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
        'stock',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/stock_inventory.yml',
    ],
}

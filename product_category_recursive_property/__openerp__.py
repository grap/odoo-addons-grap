# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category - Recursive property for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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
    'name': 'Product Category - Recursive property',
    'version': '0.1',
    'summary': "Propagate recursively properties for product category",
    'category': 'Product',
    'description': """
Propagate recursively properties for product category
=====================================================
Features :
----------
    * When an user set an accounting property to a product category, the
      parameter will be set to all childs;

Copyright and Licence :
-----------------------
    * 2013, Groupement Régional Alimentaire de Proximité
      (http://www.grap.coop/)
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2013, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'account',
        'stock',
    ],
    'data': [
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_category.yml',
    ],
}

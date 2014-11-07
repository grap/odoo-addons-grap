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

{
    'name': 'Point Of Sale - Tax',
    'version': '0.1',
    'category': 'Point of Sale',
    'description': """
Manage Correctly The Taxes in Point Of Sale Module
==================================================

Description:
------------
Store the taxes in pos_orders like for sale_orders so that the created account
moves keep the good tax even if the product is changed between the sale and the
session closure.


Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain)
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'depends': [
        'point_of_sale',
        'pos_rewrite_create_aml',
    ],
    'data': [
        'data/function.xml',
        'security/ir_model_access_data.yml',
        'view/view.xml'
    ],
}

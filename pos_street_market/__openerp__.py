# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Street Market module for Odoo
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
    'name': 'Point of Sale - Street Market',
    'version': '1.0',
    'category': 'Point of Sale',
    'description': """
Add some feature for users who sale in street
=============================================

Features :
----------
    * Add the possibility to change the date of a pos order;
    * Add a market place object;

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
        'point_of_sale',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups_data.yml',
        'security/ir_model_access_data.yml',
        'view/view.xml',
        'view/pos_order_view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'installable': False,
}

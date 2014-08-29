# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Select Customer module for OpenERP
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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
    'name': 'Point Of Sale - Select Customers',
    'summary': 'Allow users to select a customer in Point Of Sale',
    'version': '0.1',
    'category': 'sale',
    'description': """
Allow users to select a customer in Point Of Sale
=================================================

Functionality:
--------------
    * Allow user to set a customer to a pos order;

Maybe in a While:
-----------------
    * Possibility to create customers;
    * Possibility to change price if customer has a list price different as"""
    """ the default list price; (Big stuff);
    * Possibility to see if the partner has not the default price list;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'pos_second_header',
    ],
    'qweb': [
        'static/src/xml/psc.xml',
    ],
    'js': [
        'static/src/js/psc.js',
    ],
    'css': [
        'static/src/css/psc.css',
    ],
}

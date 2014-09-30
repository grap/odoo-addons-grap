# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Secure Front Office module for OpenERP
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
    'name': 'Point Of Sale - Secure Front Office',
    'summary': """Intend to prevent data loss if Network is down""",
    'version': '0.1',
    'category': 'sale',
    'description': """
Intend to prevent data loss if Network is down
==============================================

Functionality:
--------------
    * TODO

Maybe in a While:
-----------------
    * Disable possibility to close the window via the top button """
    """of the interface;
    * Disable possibility to hard close the window;
    * Inform the user if the network is down;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
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
        'static/src/xml/psfo.xml',
    ],
    'js': [
        'static/src/js/psfo.js',
    ],
    'css': [
        'static/src/css/psfo.css',
    ],
}

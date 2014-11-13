# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - PosBox Improvements module for Odoo
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
    'name': 'Point Of Sale - PosBox improvements',
    'version': '0.1',
    'summary': 'Improve PosBox calls from Front / Back office Point of Sale',
    'category': 'Point of Sale',
    'description': """
Improve PosBox calls from Front / Back office Point of Sale
===========================================================

Functionality:
--------------
    * Give the possibility to print the receipt of a pos order, using the"""
    """ PosBox, in the backoffice interface;
    * Improve default behaviour of point of Sale module providing"""
    """ the possibility to set the url of the posbox (Odoo 8.0 BackPort);

Limits:
-------
    * This module only emulate the behaviour of the communication between"""
    """ Odoo and the PosBox for the printers device. It could be"""
    """ to do the same thing for BarCode Scanner, Scale, etc...

TODO:
- Get proxy_ip and proxy_timeout in front office;
- Change PosModel.

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'view/view.xml',
    ],
    'js': [
        'static/src/js/pip.js',
    ],
    'qweb': [
        'static/src/xml/pip.xml',
    ],
}

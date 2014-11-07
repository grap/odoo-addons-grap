# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Improve Header module for OpenERP
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
    'name': 'Point Of Sale - Improve Header',
    'summary': 'Improve the header page of the Point Of Sale module',
    'version': '0.1',
    'category': 'sale',
    'description': """
Improve the header page of the Point Of Sale module
===================================================

Functionality:
--------------
    * Set the same css as paypad buttons for the buttons in header;
    * The button of the current pos order is in a different color to"""
    """increase visibility;

Maybe in a While:
-----------------
    * Add a scroll bar feature in the first banner to allow user to see a"""
    """ lot of pending pos order; (or block more than XX pos order ?);
    (Or more elegant solution : increase / decrease size of header dynamically
    when user adds or ends pos order; (and #content position)

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
    'css': [
        'static/src/css/pih.css',
    ],
}

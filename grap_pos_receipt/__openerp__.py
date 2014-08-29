# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Point Of Sale Receipt module for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Point Of Sale Receipt',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Point of sale : Change the receipt of the point of sale
=======================================================

Features:
---------
    * Possibility to print receipt for draft pos.order;
    * Improve of pos.receipt;
        * Reduce the size of white space;
        * Add logo of the company;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2013, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'report_webkit',
    ],
    'data': [
        'view/action.xml',
        'view/view.xml',
        'data/ir_header_webkit.xml',
        'data/ir_property.xml',
    ],
}

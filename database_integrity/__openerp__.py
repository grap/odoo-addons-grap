# -*- encoding: utf-8 -*-
##############################################################################
#
#    Database Integrity module for OpenERP
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
    'name': 'DataBase Integrity',
    'version': '0.1',
    'summary': 'Realize requests in database to check integrity',
    'category': 'Tools',
    'description': """
Realize requests in database to check integrity
===============================================

Functionality:
--------------
    * Request to know if sequences in postgres are correct;
        * Create a Wizard to view postgres sequences whose current value is"""
    """ below the max id of the table;
        * Allow possitility to admin user to fix those invalid sequences;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
}

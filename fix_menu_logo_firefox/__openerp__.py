# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fix - Logo Multi Company Firefox for Odoo
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
    'name': 'Fix - Logo multi-company (FireFox)',
    'summary': 'Fix an incorrect behaviour with firefox in multi company',
    'version': '1.0',
    'category': 'web',
    'description': """
Fix an incorrect behaviour with firefox in multi company
========================================================

Features:
---------
    * Force reloading company logo (in the menu), when the user log in,"""
    """ fixing incorrect behaviour with FireFox ;

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
        'web',
    ],
    'js': [
        'static/src/js/models.js',
    ],
}

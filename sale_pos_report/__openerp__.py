# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale / Point Of Sale Report module for OpenERP
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
    'name': 'Sale Point Of Sale - Report',
    'summary': 'Add reports merging sale and point of sale informations',
    'version': '0.1',
    'category': 'sale',
    'description': """
Add reports merging sale and point of sale informations
=======================================================

Functionality:
--------------
    * Add a graph report view in the Report menu to merge sale and point"""
    """of sale Information.

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
        'sale',
        'point_of_sale',
    ],
    'data': [
        'security/ir_model_access.yml',
        'security/ir_rule_data.xml',
        'report/sale_pos_report_view.xml',
        'report/sale_pos_report_action.xml',
        'report/sale_pos_report_menu.xml',
    ],
    'images': [
        'static/src/img/screenshots/1.png'
    ],
}

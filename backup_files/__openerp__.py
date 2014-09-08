# -*- encoding: utf-8 -*-
##############################################################################
#
#    Module - Backup Files module for Odoo
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
    'name': 'Backup Files',
    'version': '0.1',
    'summary': "Allow to get files from many servers",
    'category': 'Tools',
    'description': """
Allow to get files from many servers
====================================

Functionality:
--------------
    * This modules allows to define a new model ir.recovery that"""
    """ realize by cron, connections to servers a copy of files to a"""
    """ local folder.
    * After the backup, the module will send an email with a sumup of the"""
    """ operation. (Fail / Success, etc...)

Remark:
-------
    * This module is a Framework module;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'external_dependencies': {
        'python': ['ftplib'],
    },
}

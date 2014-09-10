# -*- encoding: utf-8 -*-
##############################################################################
#
#    Tools - Repository of Modules for Odoo
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
    'name': 'Repository of Modules',
    'version': '0.1',
    'summary': """Allows to see Repository Informations of Modules""",
    'category': 'Tools',
    'description': """
Allows to see Repository Informations of Modules
================================================

Functionality:
--------------
    * Allow to see information of repositories used by a given Database:
        * Name of the folder;
        * URL and name of the current Branch and revision ID;
        * Number of files with uncommitted modification;
        * Number of installed modules and total modules available;
    * Versioning System covered:
        * Bazaar;
        * Git;

Technical Information:
----------------------
    * This module create a new model ir.module.repository for each"""
    """ Repository defined in the addons_path parameters in the"""
    """ configuration file;
    * User has to set up an extra root_folder parameter after installing"""
    """ the module;
    * Information update is realized:
        * Automaticly, when you install or update this module;
        * Manualy, when you click on 'Update Module List';

TODO
- Gérer le _TEMP;
- Gérer le FR;
- Gérer l'import conditionnel;
- Gérer l'ir.rule pour le nouveau model;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
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
    'images': [
    ],
    'external_dependencies': {
        'python': ['git', 'bzrlib'],
    },
    'css': [
        'static/src/css/css.css',
    ]
}

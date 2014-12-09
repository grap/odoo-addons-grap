# -*- encoding: utf-8 -*-
##############################################################################
#
#    Authentification - Generate Password module for Odoo
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
    'name': 'Password Secure',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Password Secure
===============

Functionnality:
---------------
    * Forbid users to change them password;
        * Only members of base.group_system can change password; OK.
    * Add a button to the res_users form:
        * to change the password (randomly generated);
        * send an email to each users;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement R�gional Alimentaire de Proximit�;
    * Author : Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mail',
    ],
    'data': [
        'data/ir_actions_server.xml',
        'data/ir_config_parameter.yml',
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Manage accounts integrity Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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
    'name': 'Account - Manage accounts integrity',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Allow advanced possibility to manage accounts
=============================================

Features:
---------
In account modele :
    * Add a 'child_number' field to see number of direct child of an account;
    * Add a 'move_number' field to see number of move lines written in an
      account;
    * Add an 'account_ir_property' and 'account_ir_property_number' to see
      properties linked to the account;

Administration tools:
---------------------
    * Add the possibility to move all the account move from an account to
      an other;
    * Add the possibility to delete all the properties linked to an account;

Feature changes:
----------------
    * drop the unpossibility to change code or type of an account if the
      account has undirect move lines ;

Technical informations:
-----------------------
    * The administration tools are available for a new group;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account'
    ],
    'data': [
        'security/res_groups_data.yml',
        'view/action.xml',
        'view/account_action.xml',
        'view/view.xml',
        'view/account_view.xml',
    ],
    'installable': False,
}

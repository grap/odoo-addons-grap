# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Mass Drop Moves Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
    'name': 'Account - Mass Drop Moves',
    'version': '0.2',
    'summary': 'Mass Dropping of Account Moves by Period and Journal',
    'category': 'Accounting',
    'description': """
Mass Dropping of Account Moves by Period and Journal
====================================================

Features :
----------
    * Allow special user to mass drop account move, selecting a Journal and
      a Period. This feature can be usefull if you change account management
      policy.

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
        'account',
    ],
    'data': [
        'security/res_groups.yml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        #        'view/account_journal_view.xml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Move - Date and Period Conform Module for Odoo
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
    'name': 'Account Move - Date and Period Conform',
    'version': '0.2',
    'category': 'Account',
    'description': """
Prevent to have an account move with an invalid period and correct
existing moves
==================================================================
==============

Features :
----------
    * Help accounting people by filling period_id correctly when choosing
      date, period and journal;
    * Provide an interface to correct account moves with incorrect 'date'
      / 'period' values;

Technical informations :
------------------------
    * You can use 'account-financial-tools'/'account_journal_always_check_date'
      to prevent having new account moves with incorrect 'date' and 'periods'
      values;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
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
        'view/account_move_view.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        'view/account_period_view.xml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Delete Null Account Move Module for Odoo
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
    'name': 'Account - Delete Null Account Move',
    'version': '0.2',
    'category': 'Accounting',
    'description': """
Allow special user to delete null account move
==============================================

Features :
----------
    * Allow special user to delete null account move; This feature is
      interesting in the case wich OpenERP generate null account move
      (with all account move line value set to 0). This kind of account
      move has no sense for accountant people and occures when a sale is
      done with 100% discount value or if a product (with real-time valuation)
      is moved with a null standard_price.

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
        'view/account_period_view.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
}

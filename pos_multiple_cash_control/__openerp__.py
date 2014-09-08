# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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
    'name': 'Point Of Sale - Multiple Cash Control',
    'version': '2.0',
    'category': 'Point of Sale',
    'description': """
Allow the cash control on all cash registers for a session
==========================================================

Functionnality:
---------------
    * Add extra constraint on product if income_pdt or expense_pdt:
        * This product are manage by account manager only;
        * this product must have account_income (or account_expense);
        * This product must have only one VAT (if expense_pdt);
        * this product can not be 'sale_ok' or 'purchase_ok';
    * Add extra functionnality on pos_session:
        * It's now allowed to control all the payment method when user"""
    """open or close his session;

TODO:
-----
    * description;
    * test;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'point_of_sale',
        'purchase',
    ],
    'data': [
        'view/pos_box_out.xml',
        'view/pos_box_entries.xml',
        'view/point_of_sale_view.xml',
        'security/ir.model.access.csv',
        'view/pos_session_opening.xml',
        'view/account_view.xml',
        'view/account_bank_statement_line_view.xml',
        'data/product_category.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/res_users.xml',
        'demo/account_journal.yml',
        'demo/account_tax.yml',
    ]
}

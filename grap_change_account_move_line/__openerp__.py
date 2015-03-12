# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Account Move Lines Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Change Account Move Lines',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'summary': 'Various Change in Account Move Lines Generation',
    'license': 'AGPL-3',
    'description': """
Various Change in Account Move Lines Generation
===============================================
Point Of Sale:
--------------
    * Store the taxes in pos_orders like for sale_orders so that the created
      account moves keep the good tax even if the product is changed between
      the sale and the session closure; The Account Move will be valid in
      that case;


With this module, the account_move_lines (created when validating an invoice
or closing a POS session) will not be detailed by product if the
group_invoice_lines box is checked in the journal.
When you close a pos_session, it will create one account_move per day for
the sale + one account_move per payment mode.

The purpose of this module is to rewrite the awful _create_account_move_line
function of model pos_order, so that it can be easily modified by inheritance
in other modules


History:
--------
This module is the merge of:
* pos_tax;
* pos_rewrite_create_aml;
* account_group_move_lines;

Copyright, Author and Licence:
------------------------------
    * Copyright :
        * 2013-Today, GRAP - Groupement Régional Alimentaire de Proximité;
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
        'base',
        'point_of_sale',
        'pos_invoicing',
    ],
    'data': [
        'security/ir_model_access_data.yml',
        'security/ir_rule_data.yml',
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/account_tax.yml',
        'demo/product_product.yml',
        'demo/account_journal.yml',
    ],
}

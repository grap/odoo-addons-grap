# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Invoice 'Verified' state Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
    'name': "Account - Invoice 'Verified' state",
    'version': '2.0',
    'category': 'Accounting',
    'description': """
Add a 'Verified' state on account.invoice.
==========================================
    * Add a Verified state on account.invoice;
    * Only Account_manager can validate account.invoice;
    * Modify the corresponding workflow;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
    ],
    'data': [
        'account_invoice_view.xml',
        'account_invoice_workflow.xml',
    ],
}

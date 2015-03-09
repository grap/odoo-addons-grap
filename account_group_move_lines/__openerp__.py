# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Group Move Line Module for Odoo
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
    'name': 'Account - Group Move Lines',
    'version': '1.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'description': """
With this module, the account_move_lines (created when validating an invoice
or closing a POS session) will not be detailed by product if the
group_invoice_lines box is checked in the journal.
When you close a pos_session, it will create one account_move per day for
the sale + one account_move per payment mode.

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'pos_rewrite_create_aml',
        'pos_invoicing',
    ],
}

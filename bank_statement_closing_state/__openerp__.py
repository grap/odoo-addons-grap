# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Bank Statement Closing State for Odoo
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
    'name': 'Account - Bank Statement Closing State',
    'version': '2.5',
    'category': 'Point of Sale',
    'description': """
Add a "closing" state to the bank statements
============================================

So that it cannot take new lines and gives time to close it while a
new one is opened.

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
        'point_of_sale',
        'pos_multiple_cash_control',
    ],
    'data': [
        "view/bank_statement_view.xml",
        "view/pos_box_entries_view.xml",
        "view/pos_box_out_view.xml",
    ],
    'installable': True,
    'application': True,
}

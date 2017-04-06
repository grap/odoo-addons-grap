# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Change Print',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Change default reporting
========================

* account.invoice:
    * Add extra mandatory information of each line about food;
    * Remove Unit Price column and set an Unit Price VAT Exclude column;

    * On invoices that come from grouped picking, add the date of the delivery
      date.

* account.bank.statement:
    * Add the number of lines at the end of the report;

* pos.order:
    * Possibility to print receipt for draft pos.order;
    * Improve of pos.receipt;
        * Reduce the size of white space;
        * Add logo of the company;

Technical information
---------------------

change the name of the account invoice line, generated from grouped picking.


Copyright, Author and Licence
-----------------------------
    * Copyright : 2014-Today, Groupement Régional Alimentaire de Proximité;
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
        'sale_food',
        'point_of_sale',
        'report_webkit',
        'pos_improve_posbox',
        'sale_recovery_moment',
        'base',
        'report_webkit',
        'base_headers_webkit',
        'stock',
        'delivery',
        'stock_inventory_valuation',
    ],
    'data': [
        'data/report.xml',
        'data/stock_inventory_report.xml',
        'data/ir_actions_report_xml.xml',
        'view/action.xml',
        'view/view.xml',
        'data/ir_header_webkit.xml',
        'data/ir_property.xml',
    ],
}

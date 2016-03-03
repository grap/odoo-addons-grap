# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Print Product module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Print Product',
    'summary': 'Possibility to print EAN13 product',
    'version': '0.1',
    'category': 'Custom',
    'description': """
Possibility to print product information
========================================

Functionality
-------------

* Possibility to generate EAN13 code;
* Possibility to print ean13 codes;

Limits / Roadmap
----------------

* create differente model;
    * create model product.print.type:
        * margin_top;
        * margin_left;
        * inner_margin_top;
        * inner_margin_left;
        * row_qty;
        * column_qty;
        * width;
        * height;


* after V8 migration and CRB integration,
  merge odoo-addons-misc/grap_print_product
  and odoo-addons-grap/grap_change_print

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2015, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'report_webkit',
    ],
    'data': [
        'security/ir_model_access.yml',
        'report/print_product_1_report.xml',
        'views/view.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'external_dependencies': {
        'python': ['cairosvg'],
        'bin': ['wkhtmltopdf'],
    },
}

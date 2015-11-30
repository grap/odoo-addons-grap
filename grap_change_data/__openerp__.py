# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Data module for Odoo
#    Copyright (C) 2015 GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Change Data',
    'version': '1.0',
    'category': 'GRAP - Custom',
    'description': """
Change / Drop Unwished Data
===========================

Functionality
-------------

* Product Template;
    * Disable product.product_category_1;


* Change default french accounting setting:
    * 445711 : TVA collectée (Taux Plein) -> TVA collectée 20%;
    * 445712 : TVA collectée (Taux Intermédiaire) -> TVA collectée 5.5%;
    * 601 -> change from view to normal type;
    * disable some account template;

Technical Information
---------------------

* Add an 'active' field on product.category;
* Add an active field on

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
        'account',
        'l10n_fr',
    ],
    'data': [
        'data/product_category.yml',
        'data/account_account_template.xml',
        'data/account_chart_template.xml',
    ],
}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Views module for Odoo
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
    'name': 'GRAP - Change Views',
    'version': '6.0',
    'category': 'GRAP - Custom',
    'description': """
Show / Hide / change views for users
====================================

Functionality:
--------------
    * Hide a lot of field from 'basic users';
    * Change size of some columns;
    * Add product's function field in pos_category;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2013, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base',
        'base_vat',
        'delivery',
        'email_template',
        'sale_food',
        'point_of_sale',
        'pos_both_mode',
        'product',
        'product_margin',
        'product_margin_improve',
        'product_average_consumption',
        'product_theoretical_margin',
        'procurement',
        'purchase',
        'sale',
        'sale_stock',
        'stock',
        'pos_multicompany',
        'product_taxes_group',
        'sale_eshop',
        'pos_multiple_cash_control',
        'product_fiscal_company',
        'product_category_recursive_property',
        'l10n_fr',
        'sale_order_dates',
        'sale_recovery_moment',
        'pos_order_pricelist_change',
        'grap_cooperative',
        'web_dashboard_tile',
        'stock_picking_mass_assign',
        'product_ean_duplicates',
    ],
    'data': [
        'security/res_groups.yml',
        'view/account.xml',
        'view/base.xml',
        'view/grap_change_views.xml',
        'view/point_of_sale.xml',
        'view/product.xml',
        'view/purchase.xml',
        'view/sale.xml',
        'view/stock.xml',
    ],
    'css': [
        'static/src/css/css.css',
    ],
}

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
        'account_statement_reconciliation',
        'base_vat',
        'crm',
        'delivery',
        'mail',
        'email_template',
        'sale_food',
        'point_of_sale',
        'product',
        'product_margin',
        'product_margin_improve',
        'product_average_consumption',
        'product_standard_margin',
        'procurement',
        'purchase',
        'sale',
        'sale_margin',
        'sale_stock',
        'stock',
        'knowledge',
        'pos_multicompany',
        'product_taxes_group',
        'sale_eshop',
        'product_to_scale_bizerba',
        'product_fiscal_company',
        'product_category_recursive_property',
        'l10n_fr',
        'sale_order_dates',
        'sale_recovery_moment',
        'pos_order_pricelist_change',
        'grap_cooperative',
        'web_dashboard_tile',
        'stock_picking_mass_action',
        'product_ean_duplicates',
        'simple_tax_account',
        'simple_tax_sale',
        'simple_tax_purchase',
        'purchase_discount',
        'intercompany_trade_base',
        'recurring_consignment',
        'purchase_compute_order',
        'grap_change_access',
        'grap_reporting',
        'grap_print_product',
#        'barcodes_generator_product',
    ],
    'data': [
        'security/res_groups.yml',
        'view/view_account_bank_statement.xml',
        'view/view_account_invoice.xml',
        'view/view_account_invoice_line.xml',
        'view/view_account_move.xml',
        'view/view_account_move_line.xml',
        'view/view_account_tax_template.xml',
        'view/view_account_voucher.xml',
        'view/view_stock_inventory.xml',
        'view/view_stock_move.xml',
        'view/view_stock_picking.xml',
        'view/view_pos_category.xml',
        'view/view_pos_order.xml',
        'view/view_pos_order_line.xml',
        'view/view_pos_session.xml',
        'view/view_product_product.xml',
        'view/view_product_category.xml',
        'view/base.xml',
        'view/crm.xml',
        'view/grap_change_views.xml',
        'view/product.xml',
        'view/purchase.xml',
        'view/sale.xml',
        'view/stock.xml',
        'view/mail.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'css': [
        'static/src/css/css.css',
    ],
}

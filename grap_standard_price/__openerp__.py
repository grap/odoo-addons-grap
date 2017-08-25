# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'GRAP - Standard Price',
    'version': '8.0.1.0.0',
    'category': 'Custom',
    'author': "GRAP,"
              "Odoo Community Association (OCA)",
    'summary': 'Standard Price for GRAP',
    'depends': [
        'recurring_consignment',
        'product_supplierinfo_quick_edit',
        'stock_account',
        'product_supplierinfo_discount',
    ],
    'data': [
        'views/product_supplierinfo_view.xml',
        'views/product_template_view.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': True,
}

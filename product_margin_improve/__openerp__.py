# -*- coding: utf-8 -*-

{
    'name': 'Product Margin - Improve',
    'version': '0.2',
    'category': 'Product',
    'description': """
This module brings modifications to the product_margin module:
- include pos_orders in the margin calculation
- include inventory losses in the margin calculation
- take the UoM into account
- ...
=======================================================

Contacts :
----------
    * Julien WESTE;
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product_margin',
        'point_of_sale',
    ],
    'data': [
        'wizard/product_margin_view.xml',
        'view/product_margin_view.xml',
        'view/action.xml',
        'view/menu.xml',
        ],
    'application' : False,
    'installable': True,
    'sequence': 150,
}

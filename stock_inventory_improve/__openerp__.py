# -*- coding: utf-8 -*-

{
    'name': 'Stock Inventory Improve ',
    'version': '2.0',
    'category': 'Stock',
    'description': """
- Display a better message in case of uom problems, mentionning the product
- Add an option to reset the stock account when you fill the inventory with 0
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'stock',
    ],
    'data': [
        'view/view.xml',
        ],
    'installable': True,
    'application': True,
}

# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Product Theoretical Margin',
    'version': '3.0',
    'category': 'Sales',
    'description': """
Adds some calculated fields in product view displaying the theoretical margin:
- theoretical margin: (sale price HT - standard price HT) / sale price HT
================================================================================
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'stock',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'view/product_margin_view.xml',
        ],
    'installable': True,
    'application': True,
    'complexity': "easy",
}

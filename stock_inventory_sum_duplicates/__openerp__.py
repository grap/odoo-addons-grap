# -*- coding: utf-8 -*-

{
    'name': 'Stock Inventory Sum Duplicates ',
    'version': '1.0',
    'category': 'Stock',
    'description': """
If a stock.inventory has several lines with same product, lot and location, the lines will be merged and the quantities will be summed before creating the stock.moves
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
    ],
    'installable': True,
    'application': True,
}

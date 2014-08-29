# -*- coding: utf-8 -*-

{
    'name': 'GRAP - POS Payment Methods List',
    'version': '2.X',
    'category': 'Point of Sale',
    'description': """
In the pos.payment wizard, display only the payment methods defined in the pos.config.
Avoid conflicts with the other account.journal.search() calls
======================================================================================================
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
                'point_of_sale_view.xml',
        ],
    'installable': True,
    'application': True,
    'complexity': "easy",
}

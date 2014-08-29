# -*- coding: utf-8 -*-

{
    'name' : 'GRAP - Change mail management for purchases',
    'version' : '2.0',
    'category' : 'GRAP - Custom',
    'description': """
Change view of purchase
=======================

    """,
    'author' : 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends' : [
        'purchase',
    ],
    'init_xml' : [],
    'update_xml' : [
        'purchase_view.xml',
    ],
    'demo_xml': [],
    'active': False,
    'installable': True, 
    'application' : True,
    'complexity': "easy",
}

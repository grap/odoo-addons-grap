# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Sales reporting',
    'version': '1.0',
    'category': 'Sales',
    'description': """
Modify the existing Sales Analysis view.
======================================================================================================
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'view/sale_report_view.xml',
        'security/ir_rule_data.xml',
        ],
    'installable': True,
    'application': True,
    'complexity': "easy",
}

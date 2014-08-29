# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Account Statement Reconciliation',
    'version': '1.0',
    'category': 'GRAP - Account',
    'description': """
        Allow to reconcile bank statements when we receive the sheet from the bank.
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - \
    Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        ],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
        ],
    'demo_xml': [],
    'application': True,
    'complexity': "easy",
    'installable': True,
    'auto_install': False,
}

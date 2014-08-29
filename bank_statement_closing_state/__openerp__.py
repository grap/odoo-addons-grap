# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Account Bank Statement closing state',
    'version': '2.X',
    'category': 'Point of Sale',
    'description': """
Add a "closing" state to the bank statements.
=============================================
So that it cannot take new lines and gives time to close it while a new one is opened.

    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'point_of_sale',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        "view/bank_statement_view.xml",
        "view/pos_box_entries.xml",
        "view/pos_box_out.xml",
    ],
    'installable': True,
    'application': True,
}

# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Invoice \'Verified\' state',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Add a 'Verified' state on account.invoice.
==========================================
    * Add a Verified state on account.invoice ; 
    * Only Account_manager can validate account.invoice ; 
    * Modify the corresponding workflow ; 
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        "account",
        "account_voucher", 
        ],
    'init_xml': [],
    'update_xml': [
        'account_invoice_view.xml', 
        'account_invoice_workflow.xml', 
        ],
    'demo_xml': [],
    'application' : True,
    'complexity': "easy",
    'installable': True,
    'auto_install': False,
}


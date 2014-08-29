# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Change some ir.values',
    'version': '0.1',
    'category': 'GRAP - Custom',
    'description': """
Set ir.values for default feature
=================================
Features :
----------
    * Model 'res.partner' ; field : 'notification_email_send' ; value : 'comment'.

Contacts :
----------
    * Julien WESTE ;
    * Sylvain LE GAL (https://twitter.com/legalsylvain) ;
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        ],
    'init_xml': [],
    'update_xml': [
        'data/ir_values.yml',
        ],
    'demo_xml': [],
     'css': [],
    'application': True,
    'complexity': "easy",
    'installable': True,
    'auto_install': False,
}

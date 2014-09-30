# -*- coding: utf-8 -*-
{
    'name': 'Account - Move line Change view',
    'version': '1.0',
    'category': 'web',
    'description': """
Replace the weird tree view by a form view for account move line
================================================================

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
            'account',
        ],
    'data': [
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': False,
    'installable': True,
    'auto_install': False,
    'images': [],
}

# -*- coding: utf-8 -*-
{
    'name': 'Change number of account move',
    'version': '0.1',
    'category': 'Accounting',
    'description': """
Allow special user to rename account move
=========================================
Features :
----------
    * Allow special user to rename account move ; Usefull if the account move doesn't have the good numeration. (for exemple if you change account move sequence) ; 

Technical informations :
------------------------
    * change account move name with next sequence ; 
    * add in the field 'narration' the old name ; 

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
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'security/res_groups_data.yml',
        'view/view.xml',
        'view/action.xml',
    ],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

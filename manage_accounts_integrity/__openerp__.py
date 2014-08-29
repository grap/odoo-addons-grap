# -*- coding: utf-8 -*-
{
    'name': 'Manage accounts integrity',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Allow advanced possibility to manage accounts
=============================================
Features :
----------
In account modele :
    * Add a 'child_number' field to see number of direct child of an account ; 
    * Add a 'move_number' field to see number of move lines written in an account ; 
    * Add an 'account_ir_property' and 'account_ir_property_number' to see properties linked to the account ; 

Administration tools : 
    * Add the possibility to move all the account move from an account to an other ; 
    * Add the possibility to delete all the properties linked to an account ; 

Feature changes : 
    * drop the unpossibility to change code or type of an account if the account has undirect move lines ;

Technical informations :
------------------------
    * The administration tools are available for a new group ; 

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': ['account'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'security/res_groups_data.yml',
        'view/action.xml',
        'view/account_action.xml',
        'view/view.xml',
        'view/account_view.xml',
    ],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

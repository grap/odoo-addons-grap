# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################
{
    'name': 'Account Move - Date and period conform',
    'version': '0.1',
    'category': 'Account',
    'description': """
Prevent to have an account move with an invalid period and correct existing moves
=================================================================================
Features :
----------
    * Help accounting people by filling period_id correctly when choosing date, period and journal ;
    * Provide an interface to correct account moves with incorrect 'date' / 'period' values ; 

Technical informations :
------------------------
    * You can use 'account-financial-tools'/'account_journal_always_check_date' to prevent having new account moves with incorrect 'date' and 'periods' values ;

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
        'security/res_groups.yml',
        'view/account_move_view.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        'view/account_period_view.xml',
    ],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

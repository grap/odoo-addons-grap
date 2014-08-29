# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################
{
    'name': 'Account Merge moves by Patterns',
    'version': '0.1',
    'category': 'Account',
    'description': """
Add possibility to merge account moves
=============================================

Features :
----------
    * Add a batch feature to merge a lot of account moves that have the same patterns ;
    * A Pattern is defined by :
        * a company ; 
        * a list of credit accounts, a list of debit account ;
        * a Period ; 

Use Case :
----------
    *  this module can be used for exemple if OpenERP is set to generated account moves at each stock moves in real time ; 

Improve Possibilities :
-----------------------
    * It can be usefull to select an output journal to be able to distinct this special account moves ; 

Copyright and Licence :
-----------------------
    * 2014, Groupement Régional Alimentaire de Proximité (http://www.grap.coop/)
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)

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
        'security/ir_rule.xml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'view/account_move_view.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

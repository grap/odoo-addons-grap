# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################
{
    'name': 'POS Rewrite Create_aml',
    'version': '0.1',
    'category': 'Point of Sale',
    'license': 'AGPL-3',
    'description': """
The purpose of this module is to rewrite the awful _create_account_move_line 
function of model pos_order, so that it can be easily modified by inheritance
in other modules
==========================================================================

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.

    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

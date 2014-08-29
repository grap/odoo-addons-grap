# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################

{
    'name': 'Product Category - Recursive property',
    'version': '0.1',
    'category': 'Product',
    'description': """
Propagate recursively properties for product category
=====================================================
Features :
----------
    * When an user set an accounting property to a product category, the parameter will be set to all child.

Copyright and Licence :
-----------------------
    * 2014, Groupement Régional Alimentaire de Proximité (http://www.grap.coop/)
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain) ;
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'account',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'installable': True,
    'application': True,
}

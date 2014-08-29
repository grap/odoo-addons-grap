# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################
{
    'name': 'Product Category - search on complete name',
    'version': '0.1',
    'category': 'Sale',
    'description': """
Search the product_category on the complete name, that's to say the name containing all parents
=============================================

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
        'product',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'view/product_view.xml',
    ],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

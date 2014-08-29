# -*- encoding: utf-8 -*-
###############################################################################
#    See Copyright and Licence Informations undermentioned.
###############################################################################
{
    'name': 'Product - improve search',
    'version': '2.1',
    'category': 'Product',
    'description': """
-> This module slighly changes the product search function to allow multi words
search, usefull when you have a lot of products.
It uses the ":" as a separator. The order of the words you type doesn't matter.
For example, if you search "rice:ital:whit", it will find a product named
"white rice from italia 1kg"

When you install this module, all product names containing the separator will
be changed.
By default, the ':' in product names will be replaced by ''.
Those values can be changed in the model/product.py, with the _SEPARATOR and
_REPLACEMENT constants.

-> This module also provides unaccent search against the products. To activate
this, you have to:
- install postgresql-contrib package (sudo apt-get install postgresql-contrib)
- run this request as a superuser on the db you use: 
        CREATE EXTENSION unaccent;
- restart your OE server with --unaccent option
=============================================

Copyright and Licence :
-----------------------
    * Groupement Régional Alimentaire de Proximité (http://www.grap.coop/)
    * Licence: AGPL-3 (http://www.gnu.org/licenses/)

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
    'data': [
        'init/init.xml',
    ],
    'demo_xml': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}

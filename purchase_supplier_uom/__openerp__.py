# -*- encoding: utf-8 -*-
###############################################################################
#    See Copyright and Licence Informations undermentioned.
###############################################################################

{
    'name': 'Purchase - Supplier UOM',
    'version': '2.1',
    'category': 'Purchase',
    'description': """
Allow user to define the supplier uom for a product
=======================================================

Functionnality :
----------------
In product_supplierinfo, replace the fields.related by a fields.many2one.
For inheritance matters, we don't directly replace the field (if you replace
a not-stored field with a stored one, you'll get problems at each update) but
we modify it into a fields.function that sets and gets a new fields.many2one.

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
        'purchase',
    ],
    'data': [
        'view/view.xml',
        'data/function.xml',
        ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': True,
    'installable': True,
    'auto_install': False,
}

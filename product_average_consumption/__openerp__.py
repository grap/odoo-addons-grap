# -*- encoding: utf-8 -*-
###############################################################################
#    See Copyright and Licence Informations undermentioned.
###############################################################################
{
    'name': 'Product - Average Consumption',
    'version': '0.1',
    'category': 'Product',
    'license': 'AGPL-3',
    'description': """
Shows figures in the product form about the average consumption of products
==========================================================================

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
        'product',
        'stock',
    ],
    'data': [
        'view/view.xml',
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

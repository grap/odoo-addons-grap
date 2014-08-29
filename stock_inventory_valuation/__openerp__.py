# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################

{
    'name': 'Stock Inventory Valuation',
    'version': '0.1',
    'category': 'Stock',
    'description': """
Stores the product standard price on the inventory.line, so as to be able to
calculate the total valuation of one inventory.
=======================================================


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
        'stock',
    ],
    'data': [
        'data/stock_inventory_report.xml',
        'view/view.xml',
        ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application' : True,
    'installable': True,
    'auto_install': False,
}

# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################

{
    'name': 'POS Tax',
    'version': '0.1',
    'category': 'Point of Sale',
    'description': """
Store the taxes in pos_orders like for sale_orders so that the created account
moves keep the good tax even if the product is changed between the sale and the
session closure.
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
        'point_of_sale',
        'pos_rewrite_create_aml',
    ],
    'data': [
        'data/function.xml',
        'security/ir_model_access_data.yml',
        'view/view.xml'
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

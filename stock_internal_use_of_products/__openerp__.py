# -*- coding: utf-8 -*-

{
    'name': 'Stock Internal Use of products ',
    'version': '1.0',
    'category': 'Stock',
    'description': """
Allow non accountant user to declare the use of stockable products for specific uses (eg: gifts, tastings, etc.)
================================================================================================================

Features :
----------
    add a 'Internal Use' menu to register such uses
    add a 'Internal Use Line' menu mostly for reporting purposes

Technical informations :
------------------------
    add a 'Internal Use Case' menu to configure the internal use possibilities
    for each internal_use_case, you need to define an inventory-type stock_location
    
    Confirming an internal_use will create
        - 1 stock.picking
        - 1 stock.move for each internal_use.line between the 2 locations defined in the internal_use_case
        (- 1 account.move if your products are defined in real_time inventory)
        - 1 account.move to transfer the expense

Contacts :
----------
    * Julien WESTE;
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'product',
        'stock',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'data/ir_sequence.xml',
        'security/ir_model_access_data.yml',
        'security/ir_rule_data.yml',
        'view/internal_uses_view.xml',
        'view/internal_uses_action.xml',
        'view/internal_uses_menu.xml',
    ],
     'css': [
        'static/src/css/css.css'
    ],
    'installable': True,
    'application': True,
}

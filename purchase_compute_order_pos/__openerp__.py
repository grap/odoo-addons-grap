# -*- coding: utf-8 -*-

{
    'name': 'Computed Purchase Order - POS',
    'version': '0.1',
    'category': 'Purchase',
    'description': """
Glue module that allow to include draft pos_orders in the purchase_compute_order calculation.
=======================================================

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
        'purchase_compute_order',
        'point_of_sale',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'application' : True,
    'installable': True,
    'auto_install': True,
}

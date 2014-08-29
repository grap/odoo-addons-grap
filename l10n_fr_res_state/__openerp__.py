# -*- coding: utf-8 -*-
{
    'name': 'French States (Région)',
    'version': '0.1',
    'category': 'base',
    'description': """
Add French states data
======================

Functionnalities :
------------------
    * Populate the table res_country_state with the french states. (named 'Région')

Technical informations :
----------------------------------------
    * Use 3166-2:FR codifications (more detail http://fr.wikipedia.org/wiki/ISO_3166-2:FR) ; 
    * Only populate inner state ; (no Guyane, Mayotte, etc...) because there are in the res_country table ; 
    * Change res_country_state.code size. (3 to 4)

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        ],
    'init_xml': [],
    'update_xml': [
        'data/res_country_state_data.yml',
        ],
    'demo_xml': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': False,
    'installable': True,
    'auto_install': False,
    'images': ['static/src/img/screenshots/1.png'],
}

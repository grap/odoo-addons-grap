# -*- coding: utf-8 -*-
{
    'name': 'French Departments (Département)',
    'version': '0.1',
    'category': 'base',
    'description': """
Add French departments data
===========================

Functionnalities :
------------------
    * Create a new model res_country_department, sub division of the res_country_state ; 
    * Populate the table res_country_department with the french departments ; 

Technical informations :
----------------------------------------
    * Use 3166-2:FR codifications (more detail http://fr.wikipedia.org/wiki/ISO_3166-2:FR) ; 

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'l10n_fr_res_state',
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'data/res_country_department_fr_data.yml',
        'view/res_country_department_view.xml',
        'view/res_country_department_action.xml',
        'view/res_country_department_menu.xml',
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

# -*- coding: utf-8 -*-
{
    'name': 'GRAP - Ethical labels for products',
    'version': '2.0',
    'category': 'Sales',
    'description': """
Allow users to put ethical notations on products and print labels.
==================================================================

Functionnalities :
------------------
    * Add concept of label (organic, ...) and possibility to associate product to labels ; 
    * Add notation on products and various information about origin, makers, etc...
    * Possibility to print products label, with suggestion about wich products to print. (when price change for exemple) according to legal obligation.

Python librairies required :
----------------------------
* **cairosvg** : (to generate graphical notation)
apt-get install python-cairo python-cairosvg 

* **wkhtmltopdf** : (to print label only)
sudo apt-get install wkhtmltopdf 
On Debian system : 
sudo apt-get install xvfb
sudo nano /usr/bin/wkhtmltopdf.sh
  #!/usr/bin/env sh
  xvfb-run -a -s "-screen 0 640x480x16" wkhtmltopdf $*
sudo chmod 755 wkhtmltopdf.sh
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'report_webkit',
        'l10n_fr_res_department',
        'account_fiscal_company',
        ],
    'init_xml': [],
    'update_xml': [
        'data/ir_header_webkit.xml',
        'data/product_data.xml',
        'security/ir_module_category_data.xml',
        'security/res_groups_data.xml',
        'security/ir_rule_data.xml',
        'security/ir.model.access.csv',
        'view/account_action.xml',
        'view/product_view.xml',
        'view/res_company_view.xml',
        'view/grap_ethiquette_view.xml',
        'view/grap_ethiquette_action.xml',
        'view/grap_ethiquette_menu.xml',
        'report/grap_ethiquette_report_html.xml',
        'wizard/grap_ethiquette_print_wizard_view.xml',
        'wizard/grap_ethiquette_print_wizard_action.xml',
        'wizard/grap_ethiquette_print_wizard_menu.xml',
        'data/ir_property.xml',
        ],
    'demo_xml': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': True,
    'installable': True,
    'auto_install': False,
}

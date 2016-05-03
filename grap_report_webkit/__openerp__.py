# -*- encoding: utf-8 -*-

{
    'name': 'GRAP - Custom Report Webkit',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Change Report Webkits
=====================


Copyright, Author and Licence
-----------------------------
    * Copyright : 2014-Today, Groupement Régional Alimentaire de Proximité;
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
        # Reporting Modules
        'report_webkit',
        'report_custom_filename',
        # Module To report
        'sale',
        # Custom information
        'sale_food',
        'base_fiscal_company',
        'l10n_fr',
    ],
    'data': [
        'data/ir_header_webkit.xml',
        'data/sale_report.xml',
    ],
}

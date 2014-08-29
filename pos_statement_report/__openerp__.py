# -*- encoding: utf-8 -*-
###############################################################################
#    See Copyright and Licence Informations undermentioned.
###############################################################################
{
    'name': 'Point of Sale - Statement report',
    'version': '0.1',
    'category': 'Point_of_Sale',
    'description': """
Replace the basic account_statement report by a customed one.
=============================================

Copyright and Licence :
-----------------------
    * Groupement Régional Alimentaire de Proximité (http://www.grap.coop/)
    * Licence: AGPL-3 (http://www.gnu.org/licenses/)

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * <informatique@grap.coop> for any help or question about this module.

    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'data/account_statement_report.xml',
    ],
    'demo_xml': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}

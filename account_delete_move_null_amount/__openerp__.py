# -*- coding: utf-8 -*-
{
    'name': 'Account - Delete null account move',
    'version': '0.1',
    'category': 'Accounting',
    'description': """
Allow special user to delete null account move
==============================================
Features :
----------
    * Allow special user to delete null account move; This feature is interesting in the case wich OpenERP generate null account move (with all account move line value set to 0). This kind of account move has no sense for accountant people and occures when a sale is done with 100% discount value or if a product (with real-time valuation) is moved with a null standard_price.

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/res_groups.yml',
        'view/account_period_view.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

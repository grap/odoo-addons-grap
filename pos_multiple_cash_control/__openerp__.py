# -*- coding: utf-8 -*-
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Point Of Sale - Multiple Cash Control',
    'version': '8.0.3.0.0',
    'category': 'Point of Sale',
    'description': """


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
#        'account',
        'point_of_sale',
#        'purchase',
    ],
    'data': [
        'views/view_account_journal.xml',

#        'view/point_of_sale_view.xml',
#        'security/ir.model.access.csv',
#        'view/pos_session_opening.xml',
#        'view/account_view.xml',
#        'view/account_bank_statement_line_view.xml',
#        'view/action.xml',
#        'view/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/account_journal.xml',
#        'demo/account_tax.yml',
        'demo/pos_config.xml',
    ]
}

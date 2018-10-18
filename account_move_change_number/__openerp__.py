# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account - Move Change Number',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'summary': "Allow special user to rename account move",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account_cancel',
    ],
    'data': [
        'security/res_groups.xml',
        'views/view_account_move.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
}

# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Export accounting moves to EBP's accounting software",
    'version': '2.3',
    'author': 'Numérigraphe SARL,GRAP',
    'category': 'Generic Modules/Accounting',
    'description': """
This module lets you export accounting moves and accounts to flat text files
readable by 'EBP Comptabilité', an accounting software package widely spread
in France.
The files are in the text format for EBP's software, version 3 and above.

The export feature is in the form of a wizard related to accounting moves,
so that the person exporting the data can select which moves to export.

The exported moves cannot be changed or deleted anymore, but the export can
be reverted by unchecking the "exported" box.

Three pieces of configuration need to be set:
    * the company for each fiscal year;
    * the URI, user name and password of to access the EBP folders as Windows
      network shares (if you want to save the files directly in EBP folder);
    * the number of each fiscal year in these folders;

The files will be directly generated in the EBP network shares or can be
downloaded on the user's computer.
If those are properly set, the files should be imported automatically as
simulation moves by the EBP software next time the folder is opened.

The python package "smbc" must be installed on the server to use this module.

A menu allow the user to see the list of all past exports and download again
old ones if need be.
""",
    'depends': [
        'account_accountant',
        'base_fiscal_company',
        'intercompany_trade_fiscal_company',
    ],
    'external_dependencies': {
        'python': ['unidecode'],
    },
    'data': [
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
        'views/menu.xml',
        'wizard/view_wizard_res_partner_add_suffix.xml',
        'wizard/view_wizard_ebp_export.xml',
        'wizard/view_wizard_ebp_unexport.xml',
        'views/view_account_account.xml',
        'views/view_account_journal.xml',
        'views/view_account_move.xml',
        'views/view_account_tax_code.xml',
        'views/view_ebp_export.xml',
        'views/view_res_partner.xml',
    ],
}

# -*- coding: utf-8 -*-
##############################################################################
#
#    This module is copyright (C) 2010 Numérigraphe SARL. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Export accounting moves to EBP's accounting software",
    'version': '2.3',
    'author': 'Numérigraphe SARL / GRAP',
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
    ],
    'data': [
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
    ],
    'external_dependencies': {
        'python': ['pysmbc'],
    }
}

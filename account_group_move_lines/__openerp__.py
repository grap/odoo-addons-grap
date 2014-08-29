# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################
{
    'name': 'Account Group Move Lines',
    'version': '1.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'description': """
With this module, the account_move_lines (created when validating an invoice or closing a POS session) will not be detailed by product if the group_invoice_lines box is checked in the journal.
When you close a pos_session, it will create one account_move per day for the sale + one account_move per payment mode.
==========================================================================

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
        'pos_rewrite_create_aml',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'application' : True,
    'installable': True,
    'auto_install': False,
}

# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################

{
    'name': 'Mail - Send Email Bcc',
    'version': '1.0',
    'category': 'Social Network',
    'description': """
Give the possibility to users to receive each mail sent by OpenERP
==================================================================

Functionnality:
---------------
    * Add an extra field 'email_send_bcc' in res.users;
    * If Checked, for each mail the user send, the user will receive the copy in BCC mode;

Use Case:
---------
This feature can be usefull for users:
    * to be sure the mail was sent because OpenERP send mail depending of some partner parameters;
    * to have the whole conversation if the partner writes an answer and if mailbox manages thread by object;
    * to be sure smtp server works;

Copyright, Author and Licence:
------------------------------
    * Copyright: 2014, Groupement Régional Alimentaire de Proximité
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    * Licence: AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        ],
    'data': [
        'view/res_users_view.xml',
    ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': False,
    'installable': True,
    'auto_install': False,
}

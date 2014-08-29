## -*- encoding: utf-8 -*-
#################################################################################
##    See __openerp__.py file for Copyright and Licence Informations.
#################################################################################

from openerp.osv.orm import Model
from openerp.osv import fields

class res_users(Model):
    _inherit = 'res.users'

    ### Columns Section
    _columns = {
        'mail_send_bcc': fields.boolean('Send Email Bcc',
                help="""If checked, you will receive each mail in bcc mode """\
                """for each mail you will send using OpenERP.""")
    }

    _defaults = {
        'mail_send_bcc': True,
    }

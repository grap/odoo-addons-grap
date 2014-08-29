## -*- encoding: utf-8 -*-
#################################################################################
##    See __openerp__.py file for Copyright and Licence Informations.
#################################################################################

from openerp.osv.orm import Model
from email.Utils import COMMASPACE

class ir_mail_server(Model):
    _inherit = "ir.mail_server"
    
    ### Overload Section
    def send_email(self, cr, uid, message, 
            mail_server_id=None, smtp_server=None, smtp_port=None,
            smtp_user=None, smtp_password=None, smtp_encryption=None, 
            smtp_debug=False, context=None):
        ru_obj = self.pool['res.users']
        ru = ru_obj.browse(cr, uid, uid, context=context)
        if ru.mail_send_bcc:
            if message['Bcc']:
                message['Bcc'] = message['Bcc'].join(COMMASPACE, message['From'])
            else:
                message['Bcc'] = message['From']
        return super(ir_mail_server, self).send_email(cr, uid, message, 
                mail_server_id=None, smtp_server=None, smtp_port=None,
                smtp_user=None, smtp_password=None, smtp_encryption=None, 
                smtp_debug=False, context=None)

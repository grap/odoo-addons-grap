# -*- encoding: utf-8 -*-
##############################################################################
#
#    Authentification - Generate Password module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

# This line is noqa flaged, to allow users to use string functions written
# in ir_config_parameter
import string # flake8: noqa
import random

from openerp import SUPERUSER_ID
from openerp.osv.orm import Model
from openerp.tools.translate import _


class res_users(Model):
    _inherit = 'res.users'

    def generate_password(self, cr, uid, ids, context=None):
        mm_obj = self.pool['mail.mail']
        icp_obj = self.pool['ir.config_parameter']
        password_size = eval(icp_obj.get_param(
            cr, uid, 'auth_generate_password.password_size'))
        password_chars = eval(icp_obj.get_param(
            cr, uid, 'auth_generate_password.password_chars'))
        for ru in self.browse(cr, uid, ids, context=context):
            password = "".join([random.choice(
                password_chars) for n in xrange(password_size)])
            subject = _('OpenERP - Password Changed')
            body = _(
                """Your OpenERP credentials has been changed : <br />"""
                """- Login : %s<br />"""
                """- New Password : %s<br /><br />"""
                """Please,<br />"""
                """- remember this password and delete this email;<br />"""
                """- Communicate the password to your team, if you are"""
                """ many people to use the same credentials;""") % (
                    ru.login,
                    password)
            self._set_new_password(
                cr, uid, ru.id, None, password, None, context=None)
            mm_obj.create(
                cr, SUPERUSER_ID, {
                    'email_to': ru['email'],
                    'subject': subject,
                    'body_html': body})
        return {}

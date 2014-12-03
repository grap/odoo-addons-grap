# -*- encoding: utf-8 -*-
##############################################################################
#
#    Password Secure module for Odoo
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

import random
import string

from openerp import SUPERUSER_ID
from openerp.osv.orm import Model
from openerp.tools.translate import _


class res_users(Model):
    _inherit = 'res.users'

    # Private Function section
    def _translate(self, cr, lang, text):
        context = {'lang': lang}  # noqa: _() checks page for locals
        return _(text)

    def generate_password(self, cr, uid, ids, context=None):
        mm_obj = self.pool['mail.mail']
        for ru in self.browse(cr, uid, ids, context=context):
            password = "".join([random.choice(
                string.ascii_letters + string.digits) for n in xrange(6)])
            subject = self._translate(
                cr, ru['lang'], _('OpenERP - Password Changed'))
            body = self._translate(
                cr, ru['lang'],
                _("""Your OpenERP credentials has been changed.\n\n"""
                    """- Login : %s\n\n"""
                    """- New Password : %s\n\n""")) % (
                        ru.login,
                        password)
            self._set_new_password(
                cr, uid, ru.id, None, password, None, context=None)
            mm_obj.create(
                cr, SUPERUSER_ID, {
                    'email_to': ru['email'],
                    'subject': subject,
                    'body_html': '<pre>%s</pre>' % body})

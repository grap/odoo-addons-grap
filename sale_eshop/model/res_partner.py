# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

import os
import random
import string

from openerp.osv import fields
from openerp.osv.orm import Model


class res_partner(Model):
    _inherit = 'res.partner'

    _PASSWORD_LENGTH = 6
    _PASSWORD_CHARS = string.ascii_letters + '23456789'

    # Columns Section
    _columns = {
        'eshop_password': fields.char('Password on eShop', readonly=True),
        'eshop_active': fields.boolean('Can buy on eShop'),
    }

    # Defaults Section
    _defaults = {
        'eshop_active': False,
    }

    # Technical Function
    def login(self, cr, uid, login, password, context=None):
        res = self.search(cr, uid, [
            ('email', '=', login),
            ('eshop_password', '=', password),
            ('eshop_active', '=', True)], context=context)
        if res:
            return res[0]
        else:
            return False

    # View Function Section
    def button_generate_eshop_password(self, cr, uid, ids, context=None):
        for rp in self.browse(cr, uid, ids, context=context):
            random.seed = (os.urandom(1024))
            password = ''.join(random.choice(
                self._PASSWORD_CHARS) for i in range(self._PASSWORD_LENGTH))
            self.write(cr, uid, ids, {
                'eshop_password': password}, context=context)

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Database Integrity module for OpenERP
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

from os import path
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import SUPERUSER_ID


class ir_attachment(Model):
    _inherit = 'ir.attachment'

    def _get_present_on_filesystem(
            self, cr, uid, ids, name, arg, context=None):
        res = {}
        location = self.pool['ir.config_parameter'].get_param(
            cr, SUPERUSER_ID, 'ir_attachment.location')
        for ia in self.browse(cr, uid, ids, context=context):
            if ia.db_datas:
                res[ia.id] = 'OK - DATABASE'
            else:
                if ia.store_fname:
                    aPath = self._full_path(
                        cr, uid, location, ia.store_fname)
                    if path.exists(aPath):
                        res[ia.id] = ' OK - FILE'
                    else:
                        res[ia.id] = 'KO - FILE NOT FOUND'
                else:
                    res[ia.id] = 'KO - NO PATH'
        return res

    _columns = {
        'present_on_filesystem': fields.function(
            _get_present_on_filesystem, type='char',
            string='Present on File System',
            store={
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['write_date'], 10)}),
    }

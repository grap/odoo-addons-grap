# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Improve Images module for OpenERP
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv import fields
from openerp.osv.orm import Model


class product_product(Model):
    _inherit = 'product.product'

    def _get_has_image(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context=context):
            res[pp.id] = pp.image is not False
        return res

    _columns = {
        'has_image': fields.function(
            _get_has_image, type='boolean', string='Has Image'),
    }

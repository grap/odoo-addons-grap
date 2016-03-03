# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Print Product module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
import base64
import cairosvg
import StringIO
import barcode

from openerp.osv.orm import Model
from openerp.osv import fields


class product_product(Model):
    _inherit = 'product.product'

    # Fields Function Section
    def _get_ean13_image(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            if pp.ean13:
                EAN = barcode.get_barcode_class('ean13')
                ean = EAN(pp.ean13)
                fullname = ean.save(pp.ean13)
                f = open(fullname, 'r')
                output = StringIO.StringIO()
                svg = f.read()
                cairosvg.svg2png(
                    bytestring=svg, write_to=output, center_text=True, dpi=300)
                res[pp.id] = base64.b64encode(output.getvalue())
                os.remove(fullname)
            else:
                res[pp.id] = False
        return res

    _columns = {
        'ean13_image': fields.function(
            _get_ean13_image, string='Image of the EAN13', type='binary',
            store={
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['ean13'], 10)}),
    }

    # Action Section
    def generate_ean13(
            self, cr, uid, ids, context=None):
        EAN = barcode.get_barcode_class('ean13')
        pp_id = self.search(
            cr, uid, [('ean13', 'like', '22%')],
            order='ean13 desc', limit=1, context=context)
        if not pp_id:
            ean13 = EAN('220000000000')
        else:
            pp = self.browse(cr, uid, pp_id[0], context=context)
            ean13 = EAN(str(int(pp.ean13[0:12]) + 1))
        return self.write(cr, uid, ids, {'ean13': ean13}, context=context)

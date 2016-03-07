# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (<http://www.grap.coop>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

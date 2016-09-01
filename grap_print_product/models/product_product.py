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
                fullname = ean.save('/tmp/' + pp.ean13)
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
    def _generate_ean13(self, cr, uid, ids, prefix, size, context=None):
        EAN = barcode.get_barcode_class('ean13')
        pp_id = self.search(
            cr, uid, [('ean13', '=ilike', prefix + '%')],
            order='ean13 desc', limit=1, context=context)
        if not pp_id:
            # Generate the first one EAN13
            ean13 = EAN('%s%s' % (prefix, '0' * (12 - len(prefix))))
        else:
            # Create the next EAN13
            product = self.browse(cr, uid, pp_id[0], context=context)
            number = int(product.ean13[len(prefix):len(prefix) + size]) + 1
            ean13 = EAN(
                prefix + str(number).rjust(size, '0') +
                '0' * (12 - (len(prefix) + size)))
        return self.write(cr, uid, ids, {'ean13': ean13}, context=context)

    def generate_custom_ean13(self, cr, uid, ids, context=None):
        return self._generate_ean13(cr, uid, ids, '20', 10, context=context)

    def generate_weight_ean13(self, cr, uid, ids, context=None):
        return self._generate_ean13(cr, uid, ids, '21', 5, context=context)

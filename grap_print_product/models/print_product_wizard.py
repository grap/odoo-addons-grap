# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (<http://www.grap.coop>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class print_product_wizard(TransientModel):
    _name = 'print.product.wizard'

    # Fields Function Section
    def _get_print_type_id(self, cr, uid, context=None):
        ppt_obj = self.pool['print.product.type']
        ppt_ids = ppt_obj.search(
            cr, uid, [], limit=1, order='sequence desc, id', context=context)
        if ppt_ids:
            return ppt_ids[0]
        else:
            return False

    def _get_product_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    _columns = {
        'print_type_id': fields.many2one(
            'print.product.type', required=True, string='Print Configuration'),
        'product_id': fields.many2one(
            'product.product', readonly=True, required=True, string='Product'),
    }

    # Default values Section
    _defaults = {
        'print_type_id': _get_print_type_id,
        'product_id': _get_product_id,
    }

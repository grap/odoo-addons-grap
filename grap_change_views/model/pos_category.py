# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.osv import fields


class pos_category(Model):
    _inherit = 'pos.category'
    _order = 'complete_name_order'

    # Field Functions Section
    def _get_complete_name_order(
            self, cr, uid, ids, name, args, context=None):
        res = dict.fromkeys(ids, False)
        for pc in self.browse(cr, uid, ids, context=context):
            res[pc.id] = pc.complete_name
        return res

    def _get_product_qty(
            self, cr, uid, ids, name, args, context=None):
        res = dict.fromkeys(ids, False)
        for pc in self.browse(cr, uid, ids, context=context):
            res[pc.id] = len(pc.product_ids)
        return res

    # Column Section
    _columns = {
        'complete_name_order': fields.function(
            _get_complete_name_order, type='char',
            string='Complete Name Stored',
            store={
                'pos.category': (
                    lambda self, cr, uid, ids, c={}: ids, ['name'], 10)
            }),
        'product_ids': fields.one2many(
            'product.product', 'pos_categ_id', 'Products', readonly=True),
        'product_qty': fields.function(
            _get_product_qty, type='integer', string='Product Number'),
    }

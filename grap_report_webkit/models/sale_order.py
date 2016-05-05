# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class SaleOrder(Model):
    _inherit = 'sale.order'

    def _compute_vat_text(self, cr, uid, ids, args, context=None):
        res = {x:False for x in ids}
        for order in self.browse(cr, uid, ids, context=context):
            vat_excl = False
            vat_incl = False
            for line in order.order_line:
                for tax in line.tax_id:
                    if tax.price_include:
                        vat_incl = True
                    else:
                        vat_excl = True
            if vat_excl and  vat_incl:
                res[order.id] = _('(VAT Excl. / Incl.)')
            elif vat_excl:
                res[order.id] = _('(VAT Excl.)')
            elif vat_incl:
                res[order.id] = _('(VAT Incl.)')
            else:
                res[order.id] = ''
        return res

    def _compute_has_discount(self, cr, uid, ids, args, context=None):
        res = {x:False for x in ids}
        for order in self.browse(cr, uid, ids, context=context):
            for line in order.order_line:
                if line.discount:
                    res[order.id] = True
        return res

    _columns = {
        'has_discount': fields.boolean(
            string='Has Discount', compute='_compute_has_discount'),
        'vat_text': fields.char(
            string='VAT Text', compute='_compute_vat_text'),
    }

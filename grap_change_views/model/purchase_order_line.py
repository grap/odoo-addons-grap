# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class PurchaseOrderLine(Model):
    _inherit = 'purchase.order.line'

    # Column Section
    _columns = {
        'tax_ids_readonly': fields.related(
            'taxes_id', type='many2many', relation='account.tax',
            readonly=True, string='Taxes'),
    }

    def onchange_product_id(
            self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, context=None):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=date_order,
            fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit, context=context)
        res['value']['tax_ids_readonly'] =\
            res['value'].get('taxes_id', False)
        return res

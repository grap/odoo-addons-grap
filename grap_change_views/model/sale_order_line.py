# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class SaleOrderLine(Model):
    _inherit = 'sale.order.line'

    # Column Section
    _columns = {
        'tax_ids_readonly': fields.related(
            'tax_id', type='many2many', relation='account.tax',
            readonly=True, string='Taxes'),
    }

    def product_id_change(
            self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):
        res = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position,
            flag=flag, context=context)
        res['value']['tax_ids_readonly'] =\
            res['value'].get('tax_id', False)
        return res

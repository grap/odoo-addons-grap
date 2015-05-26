# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class AccountInvoiceLine(Model):
    _inherit = 'account.invoice.line'

    # Column Section
    _columns = {
        'tax_ids_readonly': fields.related(
            'invoice_line_tax_id', type='many2many', relation='account.tax',
            readonly=True, string='Taxes'),
    }

    def product_id_change(
            self, cr, uid, ids, product, uom_id, qty=0, name='',
            type='out_invoice', partner_id=False, fposition_id=False,
            price_unit=False, currency_id=False, context=None,
            company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            cr, uid, ids, product, uom_id, qty=qty, name=name,
            type=type, partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id, context=context,
            company_id=company_id)
        res['value']['tax_ids_readonly'] =\
            res['value'].get('invoice_line_tax_id', False)
        return res

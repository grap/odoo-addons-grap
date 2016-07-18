# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields


class AccountInvoiceLine(Model):
    _inherit = 'account.invoice.line'

    # Invalidation Section
    def _get_invoice_line_by_invoice(self, cr, uid, ids, context=None):
        """ids are account.invoice"""
        return self.pool['account.invoice.line'].search(
            cr, uid, [('invoice_id', 'in', ids)], context=context)

    def _get_invoice_line_by_product(self, cr, uid, ids, context=None):
        """ids are product.product"""
        return self.pool['account.invoice.line'].search(
            cr, uid, [('product_id', 'in', ids)], context=context)

    # Column Section
    _columns = {
        'tax_ids_readonly': fields.related(
            'invoice_line_tax_id', type='many2many', relation='account.tax',
            readonly=True, string='Taxes'),

        # Invoice related
        'type': fields.related(
            'invoice_id', 'type', string='Type', type='char', select=True,
            store={
                'account.invoice': (
                    _get_invoice_line_by_invoice, ['type'], 10),
            }),
        'state': fields.related(
            'invoice_id', 'state', string='Type', type='char', select=True,
            store={
                'account.invoice': (
                    _get_invoice_line_by_invoice, ['state'], 10),
            }),
        'partner_id': fields.related(
            'invoice_id', 'partner_id', string='Partner',
            relation='res.partner', type='many2one', select=True, store={
                'account.invoice': (
                    _get_invoice_line_by_invoice, ['period_id'], 10),
            }),
        'date_invoice': fields.related(
            'invoice_id', 'date_invoice', string='Date invoice', type='date',
            select=True, store={
                'account.invoice': (
                    _get_invoice_line_by_invoice, ['date_invoice'], 10),
            }),

        # product related
        'categ_id': fields.related(
            'product_id', 'categ_id', string='Category', select=True,
            relation='product.category', type='many2one', store={
                'account.invoice.line': (
                    lambda self, cr, uid, ids, c=None: ids, ['product_id'],
                    10),
                'product.product': (
                    _get_invoice_line_by_product, ['categ_id'], 10),
            }),
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

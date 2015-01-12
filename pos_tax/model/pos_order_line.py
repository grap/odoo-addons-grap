# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Tax Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

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

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp import SUPERUSER_ID


class pos_order_line(Model):
    _inherit = "pos.order.line"

    # Constants section
    MAX_RECORDS = 10000

    # Columns section
    def _amount_line_all(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = dict([(i, {}) for i in ids])
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, [
                t.tax_id for t in line.pol_tax_rel_id], price, line.qty,
                line.product_id, line.order_id.partner_id)
            tax_amount = 0
            for t in taxes['taxes']:
                tax_amount += t['amount']
            cur = line.order_id.pricelist_id.currency_id
            res[line.id]['price_subtotal'] = cur_obj.round(
                cr, uid, cur, taxes['total'])
            res[line.id]['price_subtotal_incl'] = cur_obj.round(
                cr, uid, cur, taxes['total_included'])
            res[line.id]['tax_amount'] = cur_obj.round(
                cr, uid, cur, tax_amount)
        return res

    _columns = {
        'pol_tax_rel_id': fields.one2many(
            'pos.order.line.tax.rel', 'orderline_id',
            string='Tax Relation Id'),
        # Existing Fields 'price_subtotal' and 'price_subtotal_incl'
        'price_subtotal': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Subtotal w/o Tax', store=True),
        'price_subtotal_incl': fields.function(
            _amount_line_all, multi='pos_order_line_amount', string='Subtotal',
            store=True),
        # New field 'tax_amount'
        'tax_amount': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Tax Amount', store=True),
    }

    # Private Section
    def _compute_tax(
            self, cr, uid, product_id, discount, qty, price_unit,
            context=None):
        at_obj = self.pool['account.tax']
        pp_obj = self.pool['product.product']
        pp = pp_obj.browse(cr, uid, product_id, context=context)

        price = price_unit * (1 - (discount or 0.0) / 100.0)
        taxes = at_obj.compute_all(
            cr, uid, pp.taxes_id, price, qty, product=pp, partner=False)
        tax_values = []
        for tax in taxes['taxes']:
            tax_values.append((0, 0, {
                'tax_id': tax['id'],
                'baseHT': taxes['total'],
                'amount_tax': tax['amount'],
            }))
        return tax_values

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        vals['pol_tax_rel_id'] = self._compute_tax(
            cr, uid, vals['product_id'], vals.get('discount', 0),
            vals.get('qty', 1.0), vals['price_unit'], context=context)
        res = super(pos_order_line, self).create(
            cr, uid, vals, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        vals['pol_tax_rel_id'] = [([5])]
        res = super(pos_order_line, self).write(
            cr, uid, ids, vals, context=context)
        extra_vals = {}
        for pol in self.browse(cr, uid, ids, context=context):
            extra_vals['pol_tax_rel_id'] = self._compute_tax(
                cr, uid, pol.product_id.id, pol.discount, pol.qty,
                pol.price_unit, context=context)
            super(pos_order_line, self).write(
                cr, uid, pol.id, extra_vals, context=context)
        return res

    # Init section
    def _init_pos_tax(self, cr, uid, ids=None, context=None):
        poltr_obj = self.pool['pos.order.line.tax.rel']
        at_obj = self.pool['account.tax']
        poltr_count = 0
        vat_correction_count = 0
        all_pol_ids = self.search(cr, SUPERUSER_ID, [], context=context)
        for i in range(0, len(all_pol_ids), self.MAX_RECORDS):
            pol_ids = all_pol_ids[i:i + self.MAX_RECORDS]
            for pol in self.browse(cr, SUPERUSER_ID, pol_ids, context=context):
                if pol.pol_tax_rel_id:
                    continue
                correct_vat = pol.create_date < '2014-01-01'
                # the 19,6% VAT was changed into 20% at that date, so we'll
                # have to replace the VAT we find on the product
                poltr_id = False
                price = pol.price_unit * (1 - (pol.discount or 0.0) / 100.0)
                taxes_list = []
                for t in pol.product_id.taxes_id:
                    if correct_vat and t.id in (181, 182, 183, 184):
                        if t.id == 184:  # TVA-VT-20.0-TTC
                            tax_id = at_obj.browse(cr, uid, 1)
                        elif t.id == 182:  # TVA-VT-20.0-HT
                            tax_id = at_obj.browse(cr, uid, 101)
                        elif t.id == 183:  # TVA-VT-10.0-HT
                            tax_id = at_obj.browse(cr, uid, 136)
                        elif t.id == 181:  # TVA-VT-10.0-TTC
                            tax_id = at_obj.browse(cr, uid, 134)
                    else:
                        tax_id = t
                    taxes_list.append(tax_id)

                taxes = at_obj.compute_all(
                    cr, uid, taxes_list, price, pol.qty, pol.product_id,
                    partner=False)
                amount = 0
                for tax in taxes['taxes']:
                    amount += tax['amount']
                    tax_id = tax['id']

                    values = {
                        'tax_id': tax_id,
                        'orderline_id': pol.id,
                        'baseHT': taxes['total'],
                        'amount_tax': tax['amount'],
                    }
                    poltr_id = poltr_obj.create(
                        cr, uid, values, context=context)
                    poltr_count += 1
                if abs(
                    amount
                    - (pol.price_subtotal_incl - pol.price_subtotal))\
                        >= 0.01:
                    amount =\
                        pol.price_subtotal_incl - pol.price_subtotal\
                        - amount + tax['amount']
                    poltr_obj.write(cr, uid, poltr_id, {
                        'amount_tax': amount
                    }, context=context)
                    vat_correction_count += 1
        return True

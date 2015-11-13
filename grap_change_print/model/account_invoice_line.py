# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
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

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class account_invoice_line(Model):
    _inherit = 'account.invoice.line'

    # Columns section
    def _get_extra_food_info(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for ail in self.browse(cr, uid, ids, context=context):
            res[ail.id] = ""
            product = ail.product_id
            if product:
                # Add country name
                if product.country_id:
                    res[ail.id] += _(" - Country : ")\
                        + product.country_id.name
                # Add country name
                if product.fresh_category:
                    res[ail.id] += _(" - Category : ")\
                        + product.fresh_category
                count_label = 0
                for label in product.label_ids:
                    if label.mandatory_on_invoice:
                        if count_label == 0:
                            count_label += 1
                            res[ail.id] += _(" - Label : ")
                        res[ail.id] += label.name
        return res

    def _get_price_unit_vat_excluded(
            self, cr, uid, ids, name, arg, context=None):
        at_obj = self.pool['account.tax']
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            tmp = at_obj.compute_all(
                cr, uid, line.invoice_line_tax_id,
                line.price_unit, line.quantity, line.product_id,
                line.invoice_id.partner_id)
            if tmp['taxes']:
                res[line.id] = tmp['taxes'][0]['price_unit']
            else:
                res[line.id] = line.price_unit
        return res

    _columns = {
        'extra_food_info': fields.function(
            _get_extra_food_info, type='char',
            string='Extra information for invoices'),
        'price_unit_vat_excluded': fields.function(
            _get_price_unit_vat_excluded, type='float',
            digits_compute=dp.get_precision('Purchase Price'),
            string='Unit Price VAT Excluded'),
    }

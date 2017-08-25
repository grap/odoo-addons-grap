# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _STANDARD_PRICE_METHOD = [
        ('consignment', 'Consignment'),
        ('purchase', 'From Supplier Infos'),
        ('manual', 'Manual'),
    ]

    _STANDARD_PRICE_FIELDS = [
        'manual_standard_price', 'seller_ids', 'uom_id', 'uom_po_id']

    # Columns Section
    standard_price_method = fields.Selection(
        string='Cost Price Method', selection=_STANDARD_PRICE_METHOD,
        compute='_compute_standard_price_method', store=True)

    manual_standard_price = fields.Float(
        string='Manual Cost Price',
        digits_compute=dp.get_precision('Product Price'))

    # Compute Section
    @api.multi
    @api.depends(
        'seller_ids.pricelist_ids.price', 'seller_ids.pricelist_ids.discount',
        'seller_ids.pricelist_ids.min_quantity', 'manual_standard_price',
        'consignor_partner_id')
    def _compute_standard_price_method(self):
        for template in self:
            if template.consignor_partner_id:
                template.standard_price_method = 'consignment'
            elif len(template.mapped('seller_ids.pricelist_ids')):
                template.standard_price_method = 'purchase'
            else:
                template.standard_price_method = 'manual'

    @api.multi
    def _compute_standard_price(self):
        for template in self:
            if template.standard_price_method == 'consignment':
                template.standard_price = 0
            if template.standard_price_method == 'manual':
                template.standard_price = template.manual_standard_price
            else:
                partnerinfo = False
                for seller in template.seller_ids:
                    if len(seller.pricelist_ids):
                        partnerinfo = seller.pricelist_ids[0]
                        break
                if partnerinfo:
                    factor = 1
                    if template.uom_po_id.id != template.uom_id.id:
                        # Making conversion
                        factor =\
                            template.uom_po_id.factor_inv\
                            / template.uom_id.factor_inv
                    template.standard_price = (
                        partnerinfo.price * (1 - partnerinfo.discount / 100) +
                        partnerinfo.unit_price_variation) / factor
                else:
                    template.standard_price = 0

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if set(self._STANDARD_PRICE_FIELDS).intersection(
                set(vals.keys())):
            res._compute_standard_price()
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if set(self._STANDARD_PRICE_FIELDS).intersection(
                set(vals.keys())):
            self._compute_standard_price()
        return res

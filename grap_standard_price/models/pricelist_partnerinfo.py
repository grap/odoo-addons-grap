# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PricelistPartnerinfo(models.Model):
    _inherit = 'pricelist.partnerinfo'

    unit_price_variation = fields.Float(string='Unit Price Variation')

    @api.model
    def create(self, vals):
        res = super(PricelistPartnerinfo, self).create(vals)
        res.mapped('suppinfo_id.product_tmpl_id')._compute_standard_price()
        return res

    @api.multi
    def write(self, vals):
        res = super(PricelistPartnerinfo, self).write(vals)
        self.mapped('suppinfo_id.product_tmpl_id')._compute_standard_price()
        return res

    @api.multi
    def unlink(self):
        template_obj = self.env['product.template']
        template_ids = self.mapped('suppinfo_id.product_tmpl_id').ids
        res = super(PricelistPartnerinfo, self).unlink()
        templates = template_obj.browse(template_ids)
        templates._compute_standard_price()
        return res

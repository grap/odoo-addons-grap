# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    report_extra_food_info = fields.Char(
        compute='_compute_report_extra_food_info')

    report_label_ids_info = fields.Char(
        compute='_compute_report_label_ids_info')

    @api.multi
    def _compute_report_extra_food_info(self):
        for product in self:
            info = []
            if product.country_id:
                info.append(_('Country: %s') % product.country_id.name)
            if product.fresh_category:
                info.append(_('Fresh Category: %s') % product.fresh_category)
            product.report_extra_food_info = ', '.join(info)

    @api.multi
    def _compute_report_label_ids_info(self):
        for product in self:
            label_info = product.label_ids.filtered(
                    lambda x: x.mandatory_on_invoice).mapped('code')
            product.report_label_ids_info = ', '.join(label_info)

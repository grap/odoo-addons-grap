# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pricetag_type_id = fields.Many2one(
        comodel_name='product.pricetag.type', string='Pricetag Type')

    pricetag_color = fields.Char(compute='_compute_pricetag_color')

    pricetag_organic_text = fields.Char(
        compute='_compute_pricetag_organic_text')

    pricetag_display_spider_chart = fields.Boolean(
        compute='_compute_pricetag_display_spider_chart')

    pricetag_origin = fields.Char(compute='_compute_pricetag_origin')

    report_extra_food_info = fields.Char(
        compute='_compute_report_extra_food_info')

    report_label_ids_info = fields.Char(
        compute='_compute_report_label_ids_info')

    pricetag_uom_id = fields.Many2one(
        comodel_name='product.uom', string='Pricetag UoM',
        domain="[('pricetag_available', '=', True)]",
        help="Set an alternative Unit of Mesure if you want to display"
        " the price on your pricetags relative to this Unit.")

    pricetag_price_volume = fields.Char(
        compute='_compute_pricetag_price_volume')

    pricetag_price_weight_net = fields.Char(
        compute='_compute_pricetag_price_weight_net')

    # Compute Section
    @api.multi
    def _compute_pricetag_color(self):
        for product in self:
            if product.pricetag_type_id:
                product.pricetag_color = product.pricetag_type_id.color
            else:
                product.pricetag_color = product.company_id.pricetag_color

    @api.multi
    def _compute_pricetag_organic_text(self):
        for product in self:
            res = ""
            if product.is_food:
                organic = any(product.label_ids.filtered(
                    lambda x: x.is_organic))
                if organic:
                    if product.company_id.certifier_organization_id:
                        res = _("Organic Product, certified by %s") % (
                            product.company_id.certifier_organization_id.code)
                elif not product.company_id.pricetag_ignore_organic_warning:
                    res = _("Not From Organic Farming")
            product.pricetag_organic_text = res

    @api.multi
    def _compute_pricetag_display_spider_chart(self):
        for product in self:
            notation = [
                product.social_notation,
                product.organic_notation,
                product.packaging_notation,
                product.local_notation,
                ]
            notation.remove('0')
            product.pricetag_display_spider_chart = (len(notation) >= 3)

    @api.multi
    def _compute_pricetag_origin(self):
        for product in self:
            localization_info = ""
            if product.department_id:
                localization_info = product.department_id.name
            if product.state_id:
                localization_info = product.state_id.name
            if product.country_id:
                localization_info = product.country_id.name

            if not localization_info:
                product.pricetag_origin = product.origin_description
            elif product.origin_description:
                product.pricetag_origin = "%s - %s" % (
                    localization_info, product.origin_description)

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

    @api.multi
    def _compute_pricetag_price_volume(self):
        for product in self:
            if product.volume:
                price_volume = product.list_price / product.volume
                product.price_volume = "%.2f € / L" % (
                    round(price_volume, 2).replace('.', ','))

    @api.multi
    def _compute_pricetag_price_weight_net(self):
        for product in self:
            if product.weight_net:
                price_weight_net = product.list_price / product.weight_net
                unit = "kg"
            elif product.pricetag_uom_id:
                price_weight_net =\
                    product.list_price / product.pricetag_uom_id.factor
                unit = product.pricetag_uom_id.name
            if price_weight_net:
                product.price_weight_net = "%.2f € / %s" % (
                    round(price_weight_net, 2).replace('.', ','), unit)

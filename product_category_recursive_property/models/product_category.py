# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    _PRODUCT_CATEGORY_PROPERTY_LIST = [
        'property_account_income_categ',
        'property_account_expense_categ',
        'property_stock_account_input_categ',
        'property_stock_account_output_categ',
        'property_stock_valuation_account_id',
        'property_stock_journal',
    ]

    # Overload Section
    @api.model
    def create(self, vals):
        vals.update(self._get_vals_from_parent(vals.get('parent_id', False)))
        category = super(ProductCategory, self).create(vals)
        category._propagate_properties_to_childs(vals)
        return category

    @api.multi
    def write(self, vals):
        vals.update(self._get_vals_from_parent(vals.get('parent_id', False)))
        res = super(ProductCategory, self).write(vals)
        self._propagate_properties_to_childs(vals)
        return res

    # Custom Function
    @api.multi
    def _propagate_properties_to_childs(self, vals):
        values = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            if property_name in vals.keys():
                values[property_name] = vals[property_name]
        if values and self.ids:
            self.mapped('child_id').write(vals)

    @api.model
    def _get_vals_from_parent(self, parent_id):
        res = {}
        if not parent_id:
            return res
        parent = self.browse(parent_id)
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            res[property_name] = getattr(parent, property_name).id
        return res

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category - Recursive property for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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


class product_category(Model):
    _inherit = 'product.category'

    _PRODUCT_CATEGORY_PROPERTY_LIST = [
        'property_stock_journal',
        'property_stock_account_input_categ',
        'property_stock_account_output_categ',
        'property_stock_valuation_account_id',
        'property_account_income_categ',
        'property_account_expense_categ',
    ]

    # Custom Function
    def _propagate_properties_to_childs(
            self, cr, uid, ids, vals, context=None):
        values = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            if property_name in vals.keys():
                values[property_name] = vals[property_name]
        if values:
            for pc in self.browse(cr, uid, ids, context=context):
                child_ids = [x.id for x in pc.child_id]
                self.write(cr, uid, child_ids, values, context=context)

    def _get_vals_from_parent(self, cr, uid, parent_id, context=None):
        pc = self.browse(cr, uid, parent_id, context=context)
        res = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            res[property_name] = pc[property_name].id
        return res

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        if vals.get('parent_id', False):
            vals.update(self._get_vals_from_parent(
                cr, uid, vals.get('parent_id'), context=context))
        category_id = super(product_category, self).create(
            cr, uid, vals, context=context)
        self._propagate_properties_to_childs(
            cr, uid, [category_id], vals, context=context)
        return category_id

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('parent_id', False):
            vals.update(self._get_vals_from_parent(
                cr, uid, vals.get('parent_id'), context=context))
        res = super(product_category, self).write(
            cr, uid, ids, vals, context=context)
        self._propagate_properties_to_childs(
            cr, uid, ids, vals, context=context)
        return res

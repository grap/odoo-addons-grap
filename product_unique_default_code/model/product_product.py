# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Unique Default Code module for OpenERP
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


class product_product(Model):
    _inherit = 'product.product'

    def _compute_default_code(
            self, cr, uid, pCompanyId, pCategId, context=None):
        """Return unique reference for a Product depending of company and
         category"""
        if pCompanyId:
            aPrefixCompany = self.pool.get('res.company').browse(
                cr, uid, pCompanyId, context=context).product_code_prefix
            if not aPrefixCompany:
                aPrefixCompany = 'ZZZ'
        else:
            aPrefixCompany = 'ZZZ'
        aPrefixCategory = self.pool.get('product.category').browse(
            cr, uid, pCategId, context=context).product_code_prefix
        if not aPrefixCategory:
            aPrefixCategory = 'ZZZ'

        # get the product with the prefix
        aPrefix = aPrefixCompany + '-' + aPrefixCategory + '-'
        aProductsIds = self.search(
            cr, uid, [('default_code', 'like', aPrefix), ('active', '=', 0)],
            limit=1, order='default_code desc', context=None)\
            + self.search(
                cr, uid, [('default_code', 'like', aPrefix)], limit=1,
                order='default_code desc', context=None)
        aMaxCode = 0
        for aProduct in self.browse(cr, uid, aProductsIds, context=None):
            aMaxCode = max(aMaxCode, int(aProduct.default_code[-4:]))
        return {'prefix': aPrefix, 'maxCode': aMaxCode + 1}

    # Field Function Section
    def _get_default_code(self, cr, uid, ids, field_name, arg, context=None):
        """Return unique reference for products, depending of company and
        category"""
        res = {}
        aPrefixes = {}
        for product in self.browse(cr, uid, ids, context):
            tmp = self._compute_default_code(
                cr, uid, product.company_id.id, product.categ_id.id,
                context=context)
            if tmp["prefix"] in aPrefixes:
                aPrefixes[tmp["prefix"]] += 1
            else:
                aPrefixes[tmp["prefix"]] = tmp["maxCode"]
            res[product.id] = tmp["prefix"]\
                + str(aPrefixes[tmp["prefix"]]).zfill(4)
        return res

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        """ special case where product is created by data.xml file and where
        no 'categ_id' is defined."""
        if vals.get('categ_id', None) is None:
            vals['categ_id'] = self.pool.get('ir.model.data').get_object(
                cr, uid, 'product', 'product_category_all').id
        tmp = self._compute_default_code(
            cr, uid, vals.get('company_id', None), vals['categ_id'],
            context=context)
        vals['default_code'] = tmp["prefix"] + str(tmp["maxCode"]).zfill(4)
        return super(product_product, self).create(cr, uid, vals, context)

    # Changing default_code where changing prefix category
    def _get_product_by_category(self, cr, uid, ids, context=None):
        categ_obj = self.pool.get('product.category')
        product_obj = self.pool.get('product.product')
        myCategories = categ_obj.browse(cr, uid, ids, context=context)
        myProducts = []
        for category in myCategories:
            myProducts += product_obj.search(
                cr, uid, [('categ_id', '=', category.id), ('active', '=', 0)],
                context=context) \
                + product_obj.search(
                    cr, uid, [('categ_id', '=', category.id)], context=None)
        return myProducts

    # Changing default_code where changing prefix company
    def _get_product_by_company(self, cr, uid, ids, context=None):
        company_obj = self.pool.get('res.company')
        product_obj = self.pool.get('product.product')
        myCompanies = company_obj.browse(cr, uid, ids, context=context)
        myProducts = []
        for company in myCompanies:
            myProducts += product_obj.search(
                cr, uid, [('company_id', '=', company.id), ('active', '=', 0)],
                context=None) + product_obj.search(
                    cr, uid, [('company_id', '=', company.id)], context=None)
        return myProducts

    # Columns Section
    _columns = {
        'default_code': fields.function(
            _get_default_code, type='char', string='Reference', readonly=True,
            store={
                'res.company': (
                    _get_product_by_company, ['product_code_prefix'], 10),
                'product.category': (
                    _get_product_by_category, ['product_code_prefix'], 10),
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'company_id',
                        'categ_id',
                    ], 10)
            }
        ),
    }

    # Default Section
    _defaults = {
        'default_code': None,
        'categ_id': None,
    }

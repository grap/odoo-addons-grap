# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from openerp import tools
from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class eshop_category(Model):
    _name = 'eshop.category'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    _SEPARATOR = ' / '

    # Name Function
    def name_search(
            self, cr, uid, name='', args=None, operator='ilike', context=None,
            limit=80):
        ids = []
        ids = self.search(
            cr, uid, [('complete_name', operator, name)] + args, limit=limit,
            context=context)
        return self.name_get(cr, uid, ids)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for pc in self.browse(cr, uid, ids):
            res.append((pc.id, pc.complete_name))
        return res

    # Field function Section
    def _get_complete_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for ec in self.browse(cr, uid, ids, context=context):
            res[ec.id] = self._compute_complete_name(
                cr, uid, ec.id, context=context)
        return res

    def _get_product_multi(self, cr, uid, ids, field_name, arg, context=None):
        pp_obj = self.pool['product.product']
        res = {}
        for ec in self.browse(cr, uid, ids, context):
            pp_ids = [pp.id for pp in ec.product_ids]
            available_pp_ids = pp_obj.search(
                cr, uid, [
                    ('id', 'in', pp_ids), ('eshop_ok', '=', True)],
                context=context)
            res[ec.id] = {
                'product_qty': len(pp_ids),
                'available_product_ids': available_pp_ids,
                'available_product_qty': len(available_pp_ids),
                'child_qty': len(ec.child_ids),
            }
        return res

    def _get_image_multi(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(
                obj.image, avoid_resize_medium=True)
        return result

    def _set_image_multi(self, cr, uid, id, name, value, args, context=None):
        return self.write(
            cr, uid, [id], {'image': tools.image_resize_image_big(value)},
            context=context)

    _columns = {
        'name': fields.char(
            'Name', required=True, select=True),
        'complete_name': fields.function(
            _get_complete_name, type='char', string='Name', store={
                'eshop.category': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['name', 'parent_id'], 10)}),
        'image': fields.binary(
            'Image', help="Limited to 1024x1024px."),
        'company_id': fields.many2one(
            'res.company', 'Company', select=True, required=True),
        'image_small': fields.function(
            _get_image_multi, fnct_inv=_set_image_multi,
            string='Small-sized image', type='binary', multi='_get_image',
            store={
                'eshop.category': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10)}),
        'image_medium': fields.function(
            _get_image_multi, fnct_inv=_set_image_multi,
            string='Medium-sized image', type='binary', multi='_get_image',
            store={
                'eshop.category': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10)}),
        'parent_id': fields.many2one(
            'eshop.category', 'Parent Category', select=True,
            ondelete='cascade', domain="[('type', '=', 'view')]"),
        'child_ids': fields.one2many(
            'eshop.category', 'parent_id', string='Child Categories'),
        'child_qty': fields.function(
            _get_product_multi, multi='product', type='integer',
            string='Childs Quantity'),
        'type': fields.selection(
            [('view', 'View'), ('normal', 'Normal')], 'Category Type',
            help="""A category of the view type is a virtual category that"""
            """ can be used as the parent of another category to create a"""
            """ hierarchical structure.""", required=True),
        'product_ids': fields.one2many(
            'product.product', 'eshop_category_id', string='Products'),
        'product_qty': fields.function(
            _get_product_multi, multi='product', type='integer',
            string='Products Quantity'),
        'available_product_ids': fields.function(
            _get_product_multi, multi='product', type='one2many',
            relation='product.product',
            string='Available Products'),
        'available_product_qty': fields.function(
            _get_product_multi, multi='product', type='integer',
            string='Available Products Quantity'),
    }

    _defaults = {
        'type': 'view',
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
    }

    # Constraints Section
    def _check_type(self, cr, uid, ids, context=None):
        for ec in self.browse(cr, uid, ids, context=context):
            if ec.type == 'view' and ec.product_qty > 0:
                return False
            elif ec.type == 'normal' and len(ec.child_ids) > 0:
                return False
        return True

    _constraints = [
        (_check_type,
            """Error ! A 'view' Category can not belongs products;"""
            """A 'normal' Category can not belongs childs categories.""",
            ['view']),
    ]

    # Private Function
    def _compute_complete_name(self, cr, uid, id, context=None):
        pc = self.browse(cr, uid, id, context=context)
        if pc.parent_id:
            res = self._compute_complete_name(
                cr, uid, pc.parent_id.id, context=context) \
                + self._SEPARATOR + pc.name
        else:
            res = pc.name
        return res

    # Overload Section
    def write(self, cr, uid, ids, values, context=None):
        res = super(eshop_category, self).write(
            cr, uid, ids, values, context=context)
        for ec in self.browse(cr, uid, ids, context=context):
            for ec in ec.child_ids:
                self.write(cr, uid, [ec.id], {
                    'complete_name': self._compute_complete_name(
                        cr, uid, ec.id, context=context)}, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        for ec in self.browse(cr, uid, ids, context=context):
            if len(ec.child_ids) > 0:
                raise osv.except_osv(
                    _('Category with Childs!'),
                    _("""You cannot delete the category '%s' because"""
                        """ it contents %s child categories. Please move"""
                        """ child categories to another Category First.""") % (
                            ec.name, ec.child_qty))
            if ec.product_qty > 0:
                raise osv.except_osv(
                    _('Category with Products!'),
                    _("""You cannot delete the category '%s' because"""
                        """ it contents %s products. Please move"""
                        """ products to another Category First.""") % (
                            ec.name, ec.product_qty))
        return super(eshop_category, self).unlink(
            cr, uid, ids, context=context)

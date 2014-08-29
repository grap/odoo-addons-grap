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

from lxml import etree

from openerp.osv.orm import Model
from openerp.osv import fields


class product_category(Model):
    _inherit = 'product.category'

    # Overload Section
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False):
        """Add a required modifiers on the field product_code_prefix"""
        res = super(product_category, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar)
        if view_type in ('form', 'tree')\
                and 'product_code_prefix' in res['fields']:
            res['fields']['required'] = True
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='product_code_prefix']")[0]
            node.set('modifiers', '{"required": true}')
            res['arch'] = etree.tostring(doc)
        return res

    # Columns Section
    _columns = {
        'product_code_prefix': fields.char(
            'Product code prefix', size=3,
            help="""This field is used as a prefix to generate automatic"""
            """ and unique reference for products. Warning, changing this"""
            """ value will update the 'default_code' of all the products"""
            """ of this category"""
        ),
    }

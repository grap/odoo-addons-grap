# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (<http://www.grap.coop>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.osv import fields


class print_product_type(Model):
    _name = 'print.product.type'

    _columns = {
        'name': fields.char(
            required=True, string="Name"),

        'company_id': fields.many2one(
            'res.company', string='Company'),

        'sequence': fields.integer(
            required=True, string='Sequence'),
        'page_margin_top': fields.float(
            required=True, string="Page Margin Top"),
        'page_margin_left': fields.float(
            required=True, string="Page Margin Left"),
        'inner_margin_top': fields.float(
            required=True, string="Inner Margin Top"),
        'inner_margin_left': fields.float(
            required=True, string="Inner Margin Left"),

        'row_qty': fields.integer(
            required=True, string="Row Quantity"),
        'column_qty': fields.integer(
            required=True, string="Column Quantity"),

        'label_width': fields.float(
            required=True, string="Label Width"),
        'label_height': fields.float(
            required=True, string="Label Height"),

        'barcode_top': fields.float(
            required=True, string="Barcode Top (Relative Position)"),
        'barcode_left': fields.float(
            required=True, string="Barcode Left (Relative Position)"),
        'barcode_height': fields.float(
            required=True, string="Barcode Height"),
        'barcode_width': fields.float(
            required=True, string="Barcode Width"),

        'product_name_top': fields.float(
            required=True, string="Product Name Top (Relative Position)"),
        'product_name_left': fields.float(
            required=True, string="Product Name Left (Relative Position)"),
        'product_name_height': fields.float(
            required=True, string="Product Name Height"),
        'product_name_width': fields.float(
            required=True, string="Product Name Width"),
        'product_name_font_size': fields.float(
            required=True, string="Product Name Font Size"),
    }

    # Default values Section
    _defaults = {
        'sequence': 5,
    }

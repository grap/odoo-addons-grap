# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields
import base64
import cairosvg
import StringIO
import grap_ethiquette_radar
from openerp.tools.translate import _

_FOOD_CATEGORY_KEYS = [
    ('extra', 'Extra'),
    ('1', 'Category I'),
    ('2', 'Category II'),
    ('3', 'Category III'),
    ]


class product_product(Model):
    _name = 'product.product'
    _inherit = 'product.product'

    # --- Class attributes
    """Fields list wich modification change edition_state to 'recommanded'."""
    _FieldEditionStateRecommended = [
        'name',
        'reference',
        'default_code',
        'ethiquette_social',
        'ethiquette_local',
        'ethiquette_organic',
        'ethiquette_packaging',
        'ethiquette_origin',
        'ethiquette_maker',
        'ethiquette_label_ids',
        ]
    """Fields list wich modification change edition_state to 'compulsory'."""
    _FieldEditionStateCompulsory = [
        'list_price',
        'volume',
        'weight_net',
        'uom_id',
        ]

    # Columns section
    def _get_ethiquette_price_volume(
            self, cr, uid, ids, name, arg, context=None):
        """Return the price by the volume"""
        res = {}
        if context is None:
            context = {}
        for p in self.browse(cr, uid, ids, context=context):
            if p.list_price and p.volume:
                res[p.id] = "%.2f" % round(p.list_price/p.volume, 2)
            else:
                res[p.id] = ""
        return res

    def _get_ethiquette_price_weight_net(
            self, cr, uid, ids, name, arg, context=None):
        """Return the price by the weight_net"""
        res = {}
        if context is None:
            context = {}
        for product in self.browse(cr, uid, ids, context=context):
            if product.list_price and product.weight_net:
                res[product.id] = "%.2f" % round(
                    product.list_price/product.weight_net, 2)
            else:
                res[product.id] = ""
        return res

    def _get_ethiquette_spider_chart(
            self, cr, uid, ids, field_name, arg, context=None):
        """Return image for the field 'ethiquette_spider_chart' depending"""
        """ of ethiquette_xxx values"""
        res = {}
        for product in self.browse(cr, uid, ids, context):
            codeSVG = grap_ethiquette_radar.CodeSVG % {
                'y_social': 105 - (15 * int(product.ethiquette_social)),
                'x_organic': 105 + (15 * int(product.ethiquette_organic)),
                'y_packaging': 105 + (15 * int(product.ethiquette_packaging)),
                'x_local': 105 - (15 * int(product.ethiquette_local)),
                }
            output = StringIO.StringIO()
            cairosvg.svg2png(bytestring=codeSVG, write_to=output)
            res[product.id] = base64.b64encode(output.getvalue())
        return res

    def _get_ethiquette_image(
            self, cr, uid, ids, field_name, arg, context=None):
        """Return the image to print on ethiquette"""
        res = {}
        for product in self.browse(cr, uid, ids, context):
            if int(product.ethiquette_social) or \
                    int(product.ethiquette_organic) or \
                    int(product.ethiquette_packaging) or \
                    int(product.ethiquette_local):
                res[product.id] = product.ethiquette_spider_chart
            else:
                res[product.id] = product.company_id.ethiquette_image
        return res

    def _get_ethiquette_printed_origin(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context):
            tmp = ''
            if product.ethiquette_origin:
                tmp = product.ethiquette_origin
            if product.ethiquette_origin_department:
                tmp = product.ethiquette_origin_department.name + \
                    (' - ' + tmp if tmp else '')
            if product.ethiquette_origin_country:
                tmp = product.ethiquette_origin_country.name + \
                    (' - ' + tmp if tmp else '')
            res[product.id] = tmp
        return res

    def _get_ethiquette_color(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context):
            if product.ethiquette_type:
                res[product.id] = product.ethiquette_type.ethiquette_color
            elif product.company_id.ethiquette_color:
                res[product.id] = product.company_id.ethiquette_color
            else:
                res[product.id] = "#FFFFFF"
        return res

    _columns = {
        'ethiquette_price_volume': fields.function(
            _get_ethiquette_price_volume, type="char",
            string='Price by volume'),
        'ethiquette_price_weight_net': fields.function(
            _get_ethiquette_price_weight_net, type="char",
            string='Price by weight net'),
        'ethiquette_origin_country': fields.many2one(
            'res.country', 'Origin Country',
            help="Country of production of the product"),
        'ethiquette_origin_department': fields.many2one(
            'res.country.department', 'Origin Department',
            help="Department of production of the product"),
        'ethiquette_origin': fields.char(
            'Origin Complement', size=64,
            help="Production location complementary information",),
        'ethiquette_printed_origin': fields.function(
            _get_ethiquette_printed_origin, type="text",
            string='Text about origin'),
        'ethiquette_maker': fields.char('Maker', size=64, required=False),
        'ethiquette_category': fields.selection(
            _FOOD_CATEGORY_KEYS, 'Food category of the product',
            help="""Extra - Hight Quality : product without default ; """
            """Quality I - Good Quality : Product with little defaults ; """
            """Quality II - Normal Quality : Product with default ; """
            """Quality III - Bad Quality : Use this option only in"""
            """ specific situation."""),
        'ethiquette_label_ids': fields.many2many(
            'grap.ethiquette.label', 'ethiquette_product_label_rel',
            'product_id', 'label_id', 'Labels'),
        'ethiquette_type': fields.many2one(
            'grap.ethiquette.type', 'Type of Ethiquette',
            help="select the type of product"),
        'ethiquette_color': fields.function(
            _get_ethiquette_color, type="char",
            string="Color of the background of the ethiquette"),
        'ethiquette_edition_state': fields.selection([
            ('0', 'Up to date'), ('1', 'Recommended'), ('2', 'Compulsory'),
            ('3', 'Do not print')], 'Edition state', required=True),
        'ethiquette_social': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Social notation', required=True),
        'ethiquette_local': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Local notation', required=True),
        'ethiquette_organic': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Organic notation', required=True),
        'ethiquette_packaging': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Packaging notation', required=True),
        'ethiquette_spider_chart': fields.function(
            _get_ethiquette_spider_chart, type="binary", string='Spider Chart',
            store={
                "product.product": (
                    lambda self, cr, uid, ids, context=None: ids,
                    [
                        'ethiquette_social',
                        'ethiquette_local',
                        'ethiquette_organic',
                        'ethiquette_packaging'
                    ], 10)}
            ),
        'ethiquette_image': fields.function(
            _get_ethiquette_image, type="binary",
            string='Image on the label printed'),
    }

    # Default Section
    _defaults = {
        'ethiquette_social': '0',
        'ethiquette_local': '0',
        'ethiquette_organic': '0',
        'ethiquette_packaging': '0',
        'ethiquette_edition_state': '2',
    }

    # Constraints section
    def _check_ethiquette_origin_department_country(
            self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=None):
            if pp.ethiquette_origin_department.country_id and \
                    pp.ethiquette_origin_department.country_id.id != \
                    pp.ethiquette_origin_country.id:
                return False
        return True

    _constraints = [
        (
            _check_ethiquette_origin_department_country,
            _('Error ! Department must belong to the country.'),
            ['ethiquette_origin_department', 'ethiquette_origin_country']),
    ]

    # Overloads section
    def write(self, cr, uid, ids, values, context=None):
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        minimum_value = 0
        if len(set(values.keys()).intersection(
                set(product_product._FieldEditionStateRecommended))):
            minimum_value = 1
        if len(set(values.keys()).intersection(
                set(product_product._FieldEditionStateCompulsory))):
            minimum_value = 2
        if 'ethiquette_edition_state' in values.keys() or minimum_value == 0:
            super(product_product, self).write(
                cr, uid, ids, values, context=context)
        else:
            for product in self.browse(cr, uid, ids, context=context):
                if product.ethiquette_edition_state != 4:
                    values['ethiquette_edition_state'] = str(max(
                        minimum_value,
                        int(product.ethiquette_edition_state),
                        ))
                super(product_product, self).write(
                    cr, uid, [product.id], values, context=context)
        return True

    # Views section
    def onchange_ethiquette_label_ids(
            self, cr, uid, ids, ethiquette_label_ids, ethiquette_social,
            ethiquette_local, ethiquette_organic, ethiquette_packaging,
            context):
        """Overloading 'onchange' for field 'ethiquette_label_ids'"""
        minimum_social_value = int(ethiquette_social)
        minimum_local_value = int(ethiquette_local)
        minimum_organic_value = int(ethiquette_organic)
        minimum_packaging_value = int(ethiquette_packaging)
        for label in self.pool.get('grap.ethiquette.label').browse(
                cr, uid, ethiquette_label_ids[0][2], context=context):
            minimum_social_value = max(
                minimum_social_value, int(label.minimum_social_notation))
            minimum_local_value = max(
                minimum_local_value, int(label.minimum_local_notation))
            minimum_organic_value = max(
                minimum_organic_value, int(label.minimum_organic_notation))
            minimum_packaging_value = max(
                minimum_packaging_value, int(label.minimum_packaging_notation))
        return {'value': {
            'ethiquette_social': str(minimum_social_value),
            'ethiquette_local': str(minimum_local_value),
            'ethiquette_organic': str(minimum_organic_value),
            'ethiquette_packaging': str(minimum_packaging_value),
            }}

    def onchange_ethiquette_origin_department(
            self, cr, uid, ids, ethiquette_origin_country,
            ethiquette_origin_department):
        res = {}
        if ethiquette_origin_department:
            dept = self.pool.get('res.country.department').browse(
                cr, uid, [ethiquette_origin_department])[0]
            res = {'value': {'ethiquette_origin_country': dept.country_id.id}}
        return res

    def onchange_ethiquette_origin_country(
            self, cr, uid, ids, ethiquette_origin_country,
            ethiquette_origin_department):
        res = {}
        if not ethiquette_origin_country:
            res = {'value': {'ethiquette_origin_department': None}}
        elif ethiquette_origin_department:
            dept = self.pool.get('res.country.department').browse(
                cr, uid, [ethiquette_origin_department])[0]
            if ethiquette_origin_country != dept.country_id.id:
                res = {'value': {'ethiquette_origin_department': None}}
        return res

# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields


class res_company(Model):
    _inherit = 'res.company'
    _columns = {
        'ethiquette_image': fields.binary(
            "Ethiquette logo",
            help="""This field will be printed on ethiquette. """
            """Size : 210px * 210px"""),
        'ethiquette_color': fields.char(
            'Ethiquette Color', required=True, size=7,
            help="Color of the ethiquette. Format #RRGGBB"),
    }

    _defaults = {
        'ethiquette_color': '#FFFFFF',
    }

# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


class res_company(Model):
    _inherit = 'res.company'

    _columns = {
        'pos_receipt_logo': fields.binary(
            'Point of Sale Receipt Logo',
            help="""This field will be printed on pos receipt, limited"""
            """ to 2cm * 2cm"""),
    }

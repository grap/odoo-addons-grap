# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - PosBox Improvements module for Odoo
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

from openerp.osv import fields
from openerp.osv.orm import Model


class pos_config(Model):
    _inherit = 'pos.config'

    _columns = {
        'proxy_ip': fields.char(
            'IP Address', size=45, help="""The"""
            """ hostname or ip address of the hardware proxy. """
            """This will work for back-/front- office communication."""),
        'proxy_timeout': fields.integer(
            'Proxy Time Out',
            help="""Timeout in millisecond for the communication with the """
            """proxy. This will work only for back-office communication."""),
    }

    _defaults = {
        'proxy_timeout': 5000,
        'proxy_ip': 'http://localhost:8069',
    }

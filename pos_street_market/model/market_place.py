# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Street Market module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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


class market_place(Model):
    _description = 'Market Places'
    _name = 'market.place'

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, required=True,),
        'active': fields.boolean('Active',),
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True),
    }

    # Default section
    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
    }

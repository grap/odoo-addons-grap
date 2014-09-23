# -*- encoding: utf-8 -*-
##############################################################################
#
#    Tools - Repository of Modules for Odoo
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


class sale_order(Model):
    _inherit = 'sale.order'

    # Column Section
    _columns = {
        'moment_id': fields.many2one(
            'sale.recovery.moment', 'Recovery Moment'),
        'group_id': fields.related(
            'moment_id', 'group_id', type='many2one',
            relation='sale.recovery.moment.group', string='Recovery Group'),
    }

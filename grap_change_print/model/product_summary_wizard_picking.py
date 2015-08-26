# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class ProductSummaryWizardPicking(TransientModel):
    _name = 'product.summary.wizard.picking'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'product.summary.wizard', 'Wizard', select=True),
        'picking_id': fields.many2one(
            'stock.picking.out', 'Picking', required=True, readonly=True),
        'min_date': fields.datetime(
            'Scheduled Date', readonly=True),
        'partner_id': fields.many2one(
            'res.partner', 'Partner', required=True, readonly=True),
    }

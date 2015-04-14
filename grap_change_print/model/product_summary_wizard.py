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


class ProductSummaryWizard(TransientModel):
    _name = 'product.summary.wizard'

    # Fields Function Section
    def _get_standard_price_total(
            self, cr, uid, ids, fields, arg, context=None):
        res = {}
        for psw in self.browse(cr, uid, ids, context=context):
            res[psw.id] = 0
            for pol in psw.product_line_ids:
                res[psw.id] += pol.standard_price_total
        return res

    # Fields Default Section
    def _get_picking_line_ids(self, cr, uid, context=None):
        res = []
        spo_obj = self.pool['stock.picking.out']
        spo_ids = context.get('active_ids', False)
        if spo_ids:
            for spo in spo_obj.browse(cr, uid, spo_ids, context=context):
                res.append((0, 0, {
                    'picking_id': spo.id,
                    'partner_id': spo.partner_id.id,
                    'min_date': spo.min_date,
                }))
        return res

    def _get_product_line_ids(self, cr, uid, context=None):
        res = []
        product_lines = {}
        spo_obj = self.pool['stock.picking.out']
        spo_ids = context.get('active_ids', False)
        if spo_ids:
            for spo in spo_obj.browse(cr, uid, spo_ids, context=context):
                for sm in spo.move_lines:
                    if not sm.product_id.id in product_lines.keys():
                        product_lines[sm.product_id.id] = {
                            'quantity': 0,
                            'uom_id': sm.product_id.uom_id.id,
                            'standard_price': sm.product_id.standard_price,
                        }
                    # TODO FIXME, manage different uom by stock.move
                    product_lines[sm.product_id.id]['quantity'] +=\
                        sm.product_qty

        for k, product_line in product_lines.iteritems():
            res.append((0, 0, {
                'product_id': k,
                'quantity': product_line['quantity'],
                'uom_id': product_line['uom_id'],
                'standard_price': product_line['standard_price'],
                'standard_price_total': product_line['quantity'] *
                product_line['standard_price'],
            }))
        return res

    # Columns Section
    _columns = {
        'print_summary': fields.boolean(
            'Print Summary', help="Display a summary by Products"),
        'standard_price_total': fields.function(
            _get_standard_price_total, 'Standard Price Total'),
        'print_detail': fields.boolean(
            'Print Detail', help="Display a detail by Delivery Order"),
        'picking_line_ids': fields.one2many(
            'product.summary.wizard.picking', 'wizard_id', 'Delivery Orders'),
        'product_line_ids': fields.one2many(
            'product.summary.wizard.product', 'wizard_id',
            'Products Summary'),
    }

    # Default values Section
    _defaults = {
        'print_summary': True,
        'print_detail': True,
        'picking_line_ids': _get_picking_line_ids,
        'product_line_ids': _get_product_line_ids,
    }

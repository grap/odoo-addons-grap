# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


class stock_fill_inventory(TransientModel):
    _inherit = 'stock.fill.inventory'

    _columns = {
        'set_account_zero': fields.boolean(
            "Set account valuation to zero",
            help="""If checked, the balance of the inventory account will be"""
            """ reseted to 0 after validating the inventory"""),
    }

    # OverWrite Section
    def _default_location(self, cr, uid, ids, context=None):
        sl_obj = self.pool['stock.location']
        sl_ids = sl_obj.search(cr, uid, [
            ('usage', '=', 'internal'),
            ('chained_location_type', '=', 'none')], context=context)
        if len(sl_ids) > 0:
            return sl_ids[0]
        return False

    _defaults = {
        'location_id': _default_location,
    }

    # Overload Section
    def fill_inventory(self, cr, uid, ids, context=None):
        si_id = context['active_ids'][0]
        assert(len(ids) == 1)
        res = super(stock_fill_inventory, self).fill_inventory(
            cr, uid, ids, context=context)

        # manage account to zero
        si_obj = self.pool['stock.inventory']
        sfi = self.browse(cr, uid, ids[0], context=context)

        if sfi.set_stock_zero and sfi.set_account_zero:
            si_obj.write(cr, uid, si_id, {
                'set_account_zero': True,
            }, context=context)

        # Fix price_unit to 0
        si_obj.reset_price_unit(cr, uid, [si_id], context=context)
        return res

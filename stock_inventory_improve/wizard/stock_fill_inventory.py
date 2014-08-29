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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import mute_logger

class stock_fill_inventory(osv.osv_memory):
    _inherit = "stock.fill.inventory"

    def _default_location(self, cr, uid, ids, context=None):
        try:
            location = self.pool.get('ir.model.data').get_object(cr, uid, 'stock', 'stock_location_stock')
            with mute_logger('openerp.osv.orm'):
                location.check_access_rule('read', context=context)
            location_id = location.id
        except (ValueError, orm.except_orm), e:
            return False
        return location_id or False

    _columns = {
        'set_account_zero': fields.boolean("Set account valuation to zero",help="If checked, the balance of the inventory account will be reseted to 0 after validating the inventory"),
    }

    def fill_inventory(self, cr, uid, ids, context=None):
        """ To Import stock inventory according to products available in the selected locations.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs if we want more than one
        @param context: A standard dictionary
        @return:
        """
        if context is None:
            context = {}

        res = super(stock_fill_inventory, self).fill_inventory(
                                                cr, uid, ids, context=context)
        inventory_obj = self.pool.get('stock.inventory')
        if ids and len(ids):
            ids = ids[0]
        else:
             return {'type': 'ir.actions.act_window_close'}
        fill_inventory = self.browse(cr, uid, ids, context=context)
        
        if fill_inventory.set_stock_zero and fill_inventory.set_account_zero:
            inventory_id = context['active_ids'][0]
            inventory_obj.write(cr, uid, inventory_id, {
                'set_account_zero': True,
            }, context=context)
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

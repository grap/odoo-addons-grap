# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Inventory Improve Module for Odoo
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

from openerp.osv import fields
from openerp.osv.orm import Model


class stock_inventory(Model):
    _inherit = 'stock.inventory'

    _columns = {
        'set_account_zero': fields.boolean(
            "Set account valuation to zero",
            help="""If checked, the balance of the inventory account will"""
            """ be reseted to 0 after validating the inventory"""),
    }

    # Overload section
    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_inventory, self).action_done(
            cr, uid, ids, context=context)
        set_zero = any(
            si.set_account_zero is True for si in self.browse(
                cr, uid, ids, context=context))
        if set_zero:
            # create move lines
            self._reset_stock_account(cr, uid, ids, context=context)
        return res

    # Action section
    def reset_price_unit(self, cr, uid, ids, context=None):
        sil_obj = self.pool['stock.inventory.line']
        for si in self.browse(cr, uid, ids, context=context):
            for sil in si.inventory_line_id:
                sil_obj.write(cr, uid, [sil.id], {
                    'price_unit': sil.product_id.standard_price,
                }, context=context)
        return True

    # Private section
    def _reset_stock_account(self, cr, uid, ids, context=None):
        ip_obj = self.pool['ir.property']
        am_obj = self.pool['account.move']
        ap_obj = self.pool['account.period']

        inventory = self.browse(cr, uid, ids, context=context)
        inventory = inventory and inventory[0] or False

        # get the stock accounts and journal
        stock_journal = ip_obj.get(
            cr, uid, 'property_stock_journal', 'product.category',
            context=context)
        if not stock_journal:
            return False

        valuation_account = ip_obj.get(
            cr, uid, 'property_stock_valuation_account_id',
            'product.category', context=context)
        if not valuation_account:
            return False

        # get the balance
        balance = valuation_account.balance

        period = ap_obj.find(cr, uid, dt=inventory.date, context=context)
        period = period and period[0] or False

        if balance < 0:
            input_account = ip_obj.get(
                cr, uid, 'property_stock_account_input',
                'product.template', context=context)
            if not input_account:
                input_account = ip_obj.get(
                    cr, uid, 'property_stock_account_input_categ',
                    'product.category', context=context)
            if not input_account:
                return False

            # compute account_move_lines
            debit_line_vals = {
                'name': "reset %s" % inventory.name,
                'ref': "reset account valuation for %s" % inventory.name,
                'date': inventory.date,
                'debit': -balance,
                'account_id': valuation_account.id,
                'period_id': period,
            }
            credit_line_vals = {
                'name': "reset %s" % inventory.name,
                'ref': "reset account valuation for %s" % inventory.name,
                'date': inventory.date,
                'credit': -balance,
                'account_id': input_account.id,
                'period_id': period,
            }

        elif balance > 0:
            output_account = ip_obj.get(
                cr, uid, 'property_stock_account_output',
                'product.template', context=context)
            if not output_account:
                output_account = ip_obj.get(
                    cr, uid, 'property_stock_account_output_categ',
                    'product.category', context=context)
            if not output_account:
                return False

            # compute account_move_lines
            debit_line_vals = {
                'name': "reset %s" % inventory.name,
                'ref': "reset account valuation for %s" % inventory.name,
                'date': inventory.date,
                'debit': balance,
                'account_id': output_account.id,
                'period_id': period,
            }
            credit_line_vals = {
                'name': "reset %s" % inventory.name,
                'ref': "reset account valuation for %s" % inventory.name,
                'date': inventory.date,
                'credit': balance,
                'account_id': valuation_account.id,
                'period_id': period,
            }

        else:
            return False

        # Create account_move
        am_obj.create(cr, uid, {
            'journal_id': stock_journal.id,
            'date': inventory.date,
            'period_id': period,
            'line_id': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)],
            'ref': 'reset %s' % inventory.name}, context=context)

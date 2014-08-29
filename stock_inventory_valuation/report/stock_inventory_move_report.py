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

#import time
from openerp.report import report_sxw
from stock.report import stock_inventory_move_report

class stock_inventory_move(stock_inventory_move_report.stock_inventory_move):

    def __init__(self, cr, uid, name, context):
        super(stock_inventory_move, self).__init__(cr, uid, name, context=context)
        self.total_valuation = 0
        self.localcontext.update({
            'total_valuation': self._get_total_valuation,
        })


    def _get_total_valuation(self, objects):
        total = 0.0
        for obj in objects:
            total += obj.valuation
        return total

# remove previous sale.report service :
from netsvc import Service
del Service._services['report.stock.inventory.move']

# register the new report service :
report_sxw.report_sxw(
    'report.stock.inventory.move',
    'stock.inventory',
    'addons/stock_inventory_valuation/report/stock_inventory_move.rml',
    parser=stock_inventory_move,
    header='internal'
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

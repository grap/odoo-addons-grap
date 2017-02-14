# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (c) 2011-2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi
#   Copyright (c) 2013 Agile Business Group (http://www.agilebg.com)
#   @author Lorenzo Battistini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.report import report_sxw


class StandardParser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(StandardParser, self).__init__(
            cr, uid, name, context=context)


report_sxw.report_sxw(
    'report.summary.report',
    'product.summary.wizard',
    'addons/grap_change_print/report/stock_picking_out_product_summary.mako',
    parser=StandardParser)

report_sxw.report_sxw(
    'report.webkit.delivery_order',
    'stock.picking',
    'addons/grap_change_print/report/stock_picking_out_delivery_order.mako',
    parser=StandardParser)

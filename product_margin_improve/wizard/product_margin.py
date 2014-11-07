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

from openerp.osv import fields, osv


class product_margin(osv.osv_memory):
    _inherit = 'product.margin'
    _columns = {
        'pos_state': fields.selection([
            ('done', 'Done'),
            ('done_paid', 'Done and Paid'),
            ('draft_done_paid', 'Draft, Done and Paid'),
        ], 'POS Order State', select=True, required=True),
        'invoice_state': fields.selection([
            ('paid', 'Paid'),
            ('verified_paid', 'Verified and Paid'),
            ('open_verified_paid', 'Open, Verified and Paid'),
            ('draft_open_verified_paid', 'Draft, Open, Verified and Paid'),
        ], 'Invoice State', select=True, required=True),
    }

    _defaults = {
        'pos_state': "done_paid",
        'invoice_state': "open_verified_paid",
    }

    # Overwrite section
    def action_open_window(self, cr, uid, ids, context=None):
        """
            @param cr: the current row, from the database cursor,
            @param uid: the current user’s ID for security checks,
            @param ids: the ID or list of IDs if we want more than one

            @return:
        """
        if context is None:
            context = {}
        res = super(product_margin, self).action_open_window(
            cr, uid, ids, context=context)
        if not res:
            return False

        if context.get('mode', 'product') == 'category':
            graph_view = 'product.margin.categ.graph'
            form_view = 'product.margin.categ.form'
            tree_view = 'product.margin.categ.tree'
            model = 'product.category'
        else:
            graph_view = 'product.margin.graph'
            form_view = 'product.margin.form.improve'
            tree_view = 'product.margin.tree'
            model = 'product.product'
        cr.execute(
            'select id,name from ir_ui_view where name=%s and type=%s',
            (graph_view, 'graph'))
        view_res3 = cr.fetchone()[0]
        cr.execute(
            'select id,name from ir_ui_view where name=%s and type=%s',
            (form_view, 'form'))
        view_res2 = cr.fetchone()[0]
        cr.execute(
            'select id,name from ir_ui_view where name=%s and type=%s',
            (tree_view, 'tree'))
        view_res = cr.fetchone()[0]

        res['views'] = [
            (view_res, 'tree'),
            (view_res2, 'form'),
            (view_res3, 'graph')]
        res['res_model'] = model
        return res

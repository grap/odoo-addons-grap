# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>)
#    Some modification has been realized by GRAP:
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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

from openerp.osv import osv, fields
from openerp.osv.orm import TransientModel
from tools.translate import _


class pos_box_entries(TransientModel):
    _name = 'pos.box.entries'
    _description = 'Pos Box Entries'

    def _select_cash_registers(self, cr, uid, context=None):
        if not context:
            context = {}
        abs_obj = self.pool['account.bank.statement']
        session_id = context.get('active_id', False)
        statement_ids = abs_obj.search(
            cr, uid, [('pos_session_id', '=', session_id)], context=context)
        statements = abs_obj.read(
            cr, uid, statement_ids, ['name', 'id', 'journal_id'],
            context=context)
        result = [
            (st['id'], st['journal_id'][1]
                + ' - (' + st['name'] + ')') for st in statements]
        return result

    _columns = {
        'name': fields.related('product_id', 'name', type='char', store=True),
        'statement_id': fields.selection(
            _select_cash_registers, string="Cash Register", type="many2one",
            relation='account.bank.statement', method=True, required=True),
        'session_id': fields.many2one('pos.session', 'session'),
        'product_id': fields.many2one(
            'product.product', 'Operation', required=True),
        'amount': fields.float(
            'Amount', digits=(16, 2), required=True,
            help="The amount you take in your cash register"),
        'ref': fields.char('Ref', size=32),
    }

    _defaults = {
        'session_id': (
            lambda self, cr, uid, context: context.get('active_id', False)),
    }

    # Private section
    def get_in(self, cr, uid, ids, context=None):
        abs_obj = self.pool['account.bank.statement']
        absl_obj = self.pool['account.bank.statement.line']
        for pbe in self.browse(cr, uid, ids, context=context):
            vals = {}
            statement_id = pbe.statement_id
            if not statement_id:
                raise osv.except_osv(
                    _('Error !'), _('You have to open at least one cashbox'))
            product = pbe.product_id
            acc_id = (
                product.property_account_income or
                product.categ_id.property_account_income_categ)
            if not acc_id:
                raise osv.except_osv(
                    _('Error !'),
                    _('Please check that income account is set to %s') % (
                        product.name))
            statement = abs_obj.browse(
                cr, uid, int(statement_id), context=context)
            vals['statement_id'] = statement_id
            vals['journal_id'] = int(statement.journal_id.id)
            if acc_id:
                vals['account_id'] = acc_id.id
            if pbe.amount > 0:
                vals['amount'] = pbe.amount
            else:
                vals['amount'] = - pbe.amount
            vals['ref'] = "%s" % (pbe.name or '')
            vals['name'] = "%s " % (pbe.name or '')
            absl_obj.create(cr, uid, vals, context=context)
        return {}

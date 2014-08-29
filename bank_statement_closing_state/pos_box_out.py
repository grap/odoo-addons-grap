# -*- coding: utf-8 -*-
##############################################################################
##############################################################################

import time

from osv import osv, fields
from tools.translate import _

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pos_box_entries


def get_statement(self, cr, uid, context=None): 
    """
         Make the selection list of "Open" or "Closing" statements  .
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return :Return the list of statements
    """

    statement_obj = self.pool.get('account.bank.statement')
    obj_ids = statement_obj.search(cr, uid, ['|',('state', '=', 'open'),('state', '=', 'closing'), ('user_id', '=', uid)], context=context)
    res = statement_obj.read(cr, uid, obj_ids, ['id', 'name', 'state'], context=context)
    res = [(r['id'], r['name'] + ' - ' + _(r['state'])) for r in res]
    if not len(res):
        raise osv.except_osv(_('Error !'), _('You do not have any open cash register. You must create a payment method or open a cash register.'))
    return res

class pos_box_out(osv.osv_memory):
    _inherit = 'pos.box.out'
    
    def _get_journal(self, cr, uid, ids, field_name = 'journal_id', arg = None, context = None):
        statements = self.pool.get('account.bank.statement').browse(cr, uid, ids, context = context)
        res = {}
        for statement in statements:
            res[statement.journal_id.id] = statement.journal_id.id
        return res 

    _columns = {
        'statement_id': fields.selection(get_statement, "Cash Register", required=True, size=-1),
        'journal_id': fields.function(_get_journal, store=True),
    }

    def get_out(self, cr, uid, ids, context=None):
        """
         Create the entries in the CashBox   .
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return :Return of operation of product
        """
        statement_obj = self.pool.get('account.bank.statement')
        res_obj = self.pool.get('res.users')
        product_obj = self.pool.get('product.product')
        statement_line_obj = self.pool.get('account.bank.statement.line')
        for data in  self.read(cr, uid, ids, context=context):
            vals = {}
            curr_company = res_obj.browse(cr, uid, uid, context=context).company_id.id
            statement_id = [data['statement_id']]
            if not statement_id:
                raise osv.except_osv(_('Error !'), _('You have to open at least one cashbox'))
            product = product_obj.browse(cr, uid, data['product_id'], context=context)
            acc_id = product.property_account_expense or product.categ_id.property_account_expense_categ
            if not acc_id:
                raise osv.except_osv(_('Error !'), _('please check that account is set to %s')%(product.name))
            if statement_id:
                statement_id = statement_id[0]
            if not statement_id:
                statement_id = statement_obj.create(cr, uid, {
                                    'date': time.strftime('%Y-%m-%d 00:00:00'),
                                    'journal_id': data['journal_id'],
                                    'company_id': curr_company,
                                    'user_id': uid,
                                }, context=context)

            vals['statement_id'] = data['statement_id']
            vals['journal_id'] = data['journal_id']
            vals['account_id'] = acc_id.id
            amount = data['amount'] or 0.0
            if data['amount'] > 0:
                amount = -data['amount']
            vals['amount'] = amount
            vals['name'] = "%s: %s " % (product.name, data['name'])
            statement_line_obj.create(cr, uid, vals, context=context)
        return {}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

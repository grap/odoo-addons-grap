# -*- coding: utf-8 -*-

from openerp.osv import fields
from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class account_account(Model):
    _inherit = 'account.account'

    # Columns section
    def _get_child_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT parent_id, count(*) as quantity
                FROM account_account
                WHERE parent_id in (%s) AND active = 'True'
                group by parent_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res

    def _search_child_number(self, cr, uid, obj, name, arg, context=None):
        if type(arg[0][2]) == bool:
            raise except_orm(_("expression is not what we expect !"), str(arg) )
        sql_req= """
        SELECT * FROM (
            SELECT aa.id, 
                CASE WHEN calc.quantity is null THEN 0 ELSE calc.quantity END as quantity
            FROM account_account as aa
            LEFT OUTER JOIN (
                SELECT parent_id, count(*) as quantity
                FROM account_account
                GROUP BY parent_id) as calc
            ON aa.id = calc.parent_id) as calc_final
            WHERE calc_final.quantity %s %s;""" %(arg[0][1], arg[0][2])
        cr.execute(sql_req)
        res = cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    def _get_move_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT account_id, count(*) as quantity
                FROM account_move_line
                WHERE account_id in (%s)
                group by account_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res

    def _get_invoice_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT account_id, count(*) as quantity
                FROM account_invoice
                WHERE account_id in (%s)
                group by account_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res

    def _get_voucher_line_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT account_id, count(*) as quantity
                FROM account_voucher_line
                WHERE account_id in (%s)
                group by account_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res
 
    def _get_closed_period_move_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT account_id, count(*) as quantity
                FROM account_move_line aml
                INNER JOIN account_period ap 
                ON ap.id = aml.period_id
                WHERE account_id in (%s)
                AND ap.state in ('done')
                GROUP BY account_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res

    def _get_reconciled_move_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = 0
        sql_req= """
                SELECT account_id, count(*) as quantity
                FROM account_move_line
                WHERE account_id in (%s)
                AND reconcile_id is not NULL
                GROUP BY account_id
                """ % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res

    def _search_move_number(self, cr, uid, obj, name, arg, context=None):
        if type(arg[0][2]) == bool:
            raise except_orm(_("expression is not what we expect !"), str(arg) )
        sql_req= """
        SELECT * FROM (
            SELECT aa.id, 
                CASE WHEN calc.quantity is null THEN 0 ELSE calc.quantity END as quantity
            FROM account_account as aa
            LEFT OUTER JOIN (
                SELECT account_id, count(*) as quantity
                FROM account_move_line
                group by account_id) as calc
            ON aa.id = calc.account_id) as calc_final
            WHERE calc_final.quantity %s %s;""" %(arg[0][1], arg[0][2])
        cr.execute(sql_req)
        res = cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    def _get_account_ir_property(self, cr, uid, ids, name, arg, context=None):
        result = {}
        ir_property_obj = self.pool.get('ir.property')
        for id in ids:
            result.setdefault(id, [])
            property_ids = ir_property_obj.search(cr, uid, [('value_reference', '=', 'account.account,%s'%(id))])
            for property_id in property_ids:
                result[id].append(property_id)
        return result

    def _get_account_ir_property_number(self, cr, uid, ids, name, arg, context=None):
        result = {}
        account_ir_property = self._get_account_ir_property(cr, uid, ids, name, arg, context=context)
        for id in ids: 
            result[id] = len(account_ir_property[id])
        return result

    def _search_account_ir_property_number(self, cr, uid, obj, name, arg, context=None):
        if type(arg[0][2]) == bool:
            raise except_orm(_("expression is not what we expect !"), str(arg) )
        sql_req= """
            SELECT
                id,
                CASE WHEN tmp.quantity is null THEN 0 ELSE tmp.quantity END as quantity
            FROM account_account 
            LEFT OUTER JOIN (
                SELECT account_id, count(*) as quantity
                FROM (
                    SELECT CAST(substring(value_reference from 17) AS INTEGER) AS account_id
                    FROM ir_property 
                    WHERE value_reference LIKE 'account.account,%%' ) AS property
                GROUP BY account_id) AS tmp
            ON id = account_id
            WHERE quantity %s %s;""" %(arg[0][1], arg[0][2])
        cr.execute(sql_req)
        res = cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    _columns = {
        'child_number' : fields.function(
            _get_child_number, type='integer', 
            fnct_search=_search_child_number,
            string='Number of direct childs', store=False),
        'invoice_number' : fields.function(
            _get_invoice_number, type='integer', 
            string='Number of Invoice', store=False),
        'voucher_line_number' : fields.function(
            _get_voucher_line_number, type='integer', 
            string='Number of Voucher Line', store=False),
        'move_number' : fields.function(
            _get_move_number, type='integer', 
            fnct_search=_search_move_number,
            string='Number of account moves', store=False),
        'closed_period_move_number' : fields.function(
            _get_closed_period_move_number, type='integer', 
            string='Number of account moves', store=False),
        'reconciled_move_number' : fields.function(
            _get_reconciled_move_number, type='integer', 
            string='Number of reconciled account moves', store=False),
        'account_ir_property' : fields.function(
            _get_account_ir_property, type='one2many', relation='ir.property',
            string='Properties', store=False),
        'account_ir_property_number' : fields.function(
            _get_account_ir_property_number, type='integer', 
            fnct_search=_search_account_ir_property_number,
            string='Number of properties', store=False),
    }

    def button_delete_properties(self, cr, uid, ids, context=None):
        for account in self.browse(cr, uid, ids, context=context):
            for ir_property in account.account_ir_property:
                self.pool.get('ir.property').unlink(cr, uid, ir_property.id, context=context)
        return True

    ### OverWrite Section
    def _check_allow_type_change(self, cr, uid, ids, new_type, context=None):
        """ 
        Overwrite _check_allow_type_change to allow change from normal into 
        'consolidation' or 'view' if child has account entries
        """
        restricted_groups = ['consolidation','view']
        line_obj = self.pool.get('account.move.line')
        for account in self.browse(cr, uid, ids, context=context):
            old_type = account.type
            ### BEGIN OF CHANGE 
            # account_ids = self.search(cr, uid, [('id', 'child_of', [account.id])])
            account_ids = [account.id]
            ### END OF CHANGE
            if line_obj.search(cr, uid, [('account_id', 'in', account_ids)]):
                #Check for 'Closed' type
                if old_type == 'closed' and new_type !='closed':
                    raise osv.except_osv(_('Warning!'), _("You cannot change the type of account from 'Closed' to any other type as it contains journal items!"))
                # Forbid to change an account type for restricted_groups as it contains journal items
                if (new_type in restricted_groups):
                    raise osv.except_osv(_('Warning!'), _("You cannot change the type of account to '%s' type as it contains journal items!") % (new_type,))
        return True

    def _check_allow_code_change(self, cr, uid, ids, context=None):
        """ 
        Overwrite _check_allow_code_change to allow change of a code of 
        an account if child has account entries
        """
        line_obj = self.pool.get('account.move.line')
        for account in self.browse(cr, uid, ids, context=context):
            ### BEGIN OF CHANGE 
            # account_ids = self.search(cr, uid, [('id', 'child_of', [account.id])], context=context)
            account_ids = [account.id]
            ### END OF CHANGE
            if line_obj.search(cr, uid, [('account_id', 'in', account_ids)], context=context):
                raise osv.except_osv(_('Warning !'), _("You cannot change the code of account which contains journal items!"))
        return True

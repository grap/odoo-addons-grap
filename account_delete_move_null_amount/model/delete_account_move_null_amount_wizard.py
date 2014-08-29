# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import TransientModel
from openerp.osv import fields, osv

class delete_account_move_null_amount_wizard(TransientModel):
    _name = 'delete.account.move.null.amount.wizard'

    ### Overloading section
    def default_get(self, cr, uid, fields, context):
        am_obj = self.pool.get('account.move')
        line_ids = []
        
        res = super(delete_account_move_null_amount_wizard, self).default_get(cr, uid, fields, context=context)
        # get account move with null amount 
        cr.execute("""
                SELECT move_id
                FROM account_move_line
                WHERE period_id = %s
                GROUP BY move_id
                HAVING SUM(debit) = 0 AND SUM(credit) = 0
            """, (context.get('active_id'),))

        am_ids = map(lambda x:x[0], cr.fetchall())

        # parse list and propose correction with new valid period
        for am in am_obj.browse(cr, uid, am_ids, context=context):
            line_ids.append((0, 0, {
                'account_move_id': am.id,
                'company_id': am.company_id.id,
                'date': am.date,
                'period_id': am.period_id.id,
                'journal_id': am.journal_id.id,
                }))
            res.update({'line_ids': line_ids})
        return res

    ### Columns
    _columns = {
        'line_ids': fields.one2many('delete.account.move.null.amount.wizard.line', 'wizard_id', 'Account Moves list'),
    }

    ### Action section
    def delete_account_move(self, cr, uid, ids, context=None):
        am_obj = self.pool.get('account.move')
        for damnaw in self.browse(cr, uid, ids, context=context):
            move_ids = [x.account_move_id.id for x in damnaw.line_ids]
            am_obj.button_cancel(cr, uid, move_ids, context=context)
            am_obj.unlink(cr, uid, move_ids, context=context)
        return {}

class delete_account_move_null_amount_wizard_line(TransientModel):
    _name = 'delete.account.move.null.amount.wizard.line'
    _description = "Information about an account move to delete"

    ### Columns section
    _columns = {
        'wizard_id': fields.many2one('delete.account.move.null.amount.wizard', 'Wizard Reference', select=True),
        'account_move_id': fields.many2one('account.move', 'Account Move to delete', readonly=True),
        'period_id': fields.many2one('account.period', 'Period', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'date': fields.date('Move Date', readonly=True),

    }

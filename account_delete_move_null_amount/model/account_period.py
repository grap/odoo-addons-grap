# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class account_period(Model):
    _inherit = 'account.period'
    
    ### Field function section
    def _get_account_move_null_amount_quantity(self, cr, uid, ids, name, arg, context=None):
        """Return the number of account moves with null amount"""
        res = {}
        for id in ids:
            res[id] = 0
        cr.execute("""
            SELECT period_id, count(*) 
            FROM(
                SELECT period_id, move_id
                FROM account_move_line
                WHERE period_id in %s
                GROUP BY move_id, period_id 
                HAVING SUM(debit) = 0 AND SUM(credit) = 0
            ) temp
            GROUP BY period_id""", (tuple(ids),))
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res
        
    ### Columns section
    _columns = {
        'account_move_null_amount_quantity': fields.function(_get_account_move_null_amount_quantity, type='integer', string='Quantity of moves with null amount', ),
    }

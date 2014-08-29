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
    def _get_account_move_incorrect_date_quantity(self, cr, uid, ids, name, arg, context=None):
        """Return the number of account moves with incorrect dates"""
        res = {}
        for id in ids:
            res[id] = 0
        sql_req = """
            SELECT ap.id, count(*) from account_move am 
            INNER JOIN account_period ap on am.period_id = ap.id 
            WHERE am.date > ap.date_stop or am.date < ap.date_start
            and ap.id in (%s)
            GROUP BY ap.id""" % (str(ids).strip('[]'),)
        cr.execute(sql_req)
        for item in cr.fetchall(): 
            res[item[0]] = item[1]
        return res
        
    ### Columns section
    _columns = {
        'account_move_incorrect_date_quantity': fields.function(_get_account_move_incorrect_date_quantity, type='integer', string='Quantity of moves with incorrect period', ),
    }

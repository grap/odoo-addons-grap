# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import Model
from openerp.tools.translate import _

class account_move(Model):
    _inherit = 'account.move'
    
    def _get_period_from_date_company_id(self, cr, uid, date, company_id, context=None):
        if not context: 
            context = {}
        ctx = context.copy()
        ctx.update({'company_id': company_id, 'account_period_prefer_normal': True})
        return self.pool.get('account.period').find(cr, uid, date, context=ctx)[0]

    def onchange_date_company_journal(self, cr, uid, ids, date, company_id, journal_id, context=None):
        if not company_id or not date or not journal_id:
            return {}
        if self.pool.get('account.journal').browse(cr, uid, journal_id, context=context).allow_date:
            period_id = self._get_period_from_date_company_id(cr, uid, date, company_id, context=context)
            return {'value': {'period_id': period_id}}
        else: 
            return {}


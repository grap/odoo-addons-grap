# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc


class pos_make_payment(osv.osv_memory):
    _inherit = 'pos.make.payment'
    
    def check(self, cr, uid, ids, context=None):
        """Check the order:
        if the order is not paid: continue payment,
        if the order is paid print ticket.
        """
        context = context or {}
        order_obj = self.pool.get('pos.order')
        obj_partner = self.pool.get('res.partner')
        active_id = context and context.get('active_id', False)

        order = order_obj.browse(cr, uid, active_id, context=context)
        amount = order.amount_total - order.amount_paid
        data = self.read(cr, uid, ids, context=context)[0]
        data['journal'] = data['journal_id']

        if amount != 0.0:
            order_obj.add_payment(cr, uid, active_id, data, context=context)

        if order_obj.test_paid(cr, uid, [active_id]):
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'pos.order', active_id, 'paid', cr)
            return {'type' : 'ir.actions.act_window_close' }

        return self.launch_payment(cr, uid, ids, context=context)
        

    def _select_journals(self, cr, uid, context=None):
        if not context:
            context = {}
            
        journal_obj = self.pool.get('account.journal')
        session_obj = self.pool.get('pos.session')
        session_id = session_obj.search(cr, uid, [('state', '=', 'opened')], context = context)
        
        journal_ids = []
        
        for session in session_obj.browse(cr, uid, session_id, context):
            j_ids = [j.id for j in session.journal_ids]
            journal_ids += j_ids

        ids = journal_obj.search(cr, uid, [('id', 'in', journal_ids),('type', '=', 'cash')], context = context)
        res = journal_obj.read(cr, uid, ids, ['name', 'id'], context = context)
        res = [(r['id'], r['name']) for r in res]
            
        ids = journal_obj.search(cr, uid, [('id', 'in', journal_ids),('type', '!=', 'cash')], context = context)
        res2 = journal_obj.read(cr, uid, ids, ['name', 'id'], context = context)
        res2 = [(r['id'], r['name']) for r in res2]
        
        res += res2
        return res
        
        
    _columns = {
        'journal_id': fields.selection(_select_journals, "Journal", required=True, size=-1),
    }

    def _default_journal(self, cr, uid, context=None):
        if not context:
            context = {}
        session = False
        order_obj = self.pool.get('pos.order')
        active_id = context and context.get('active_id', False)
        if active_id:
            order = order_obj.browse(cr, uid, active_id, context=context)
            session = order.session_id
        if session:
            for journal in session.config_id.journal_ids:
                if journal.type == 'cash':
                    return journal.id
        return False
        
    _defaults = {
        'journal_id' : _default_journal,
    }

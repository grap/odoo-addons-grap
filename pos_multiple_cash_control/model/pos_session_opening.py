

from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _

from openerp.addons.point_of_sale.point_of_sale import pos_session


class pos_session_opening(osv.osv_memory):
    _inherit = 'pos.session.opening'
    
    def open_session_cb(self, cr, uid, ids, context=None):
        assert len(ids) == 1, "you can open only one session at a time"
        proxy = self.pool.get('pos.session')
        wizard = self.browse(cr, uid, ids[0], context=context)
        values = {
            'user_id' : uid,
            'config_id' : wizard.pos_config_id.id,
        }
        session_id = proxy.create(cr, uid, values, context=context)
        s = proxy.browse(cr, uid, session_id, context=context)
        if s.state=='opened':
            return self.open_ui(cr, uid, ids, context=context)
        return self._open_session(session_id)

    def open_existing_session_cb_close(self, cr, uid, ids, context=None):
        session_obj = self.pool.get('pos.session')
        session_ids = session_obj.search(cr, uid, [('state','=','closing_control')])
        if len(session_ids) > 1:
            return {
                'name': _('Session'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'pos.session',
                'domain': [('state','=','closing_control')],
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target' : 'current',
            }
            
        else:
            wf_service = netsvc.LocalService("workflow")
            wizard = self.browse(cr, uid, ids[0], context=context)
            wf_service.trg_validate(uid, 'pos.session', wizard.pos_session_id.id, 'cashbox_control', cr)
            return self.open_session_cb(cr, uid, ids, context)

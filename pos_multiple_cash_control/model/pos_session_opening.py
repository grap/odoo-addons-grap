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

from openerp import netsvc
from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class pos_session_opening(TransientModel):
    _inherit = 'pos.session.opening'

    def open_session_cb(self, cr, uid, ids, context=None):
        assert len(ids) == 1, "you can open only one session at a time"
        ps_obj = self.pool['pos.session']
        wizard = self.browse(cr, uid, ids[0], context=context)
        values = {
            'user_id': uid,
            'config_id': wizard.pos_config_id.id,
        }
        session_id = ps_obj.create(cr, uid, values, context=context)
        s = ps_obj.browse(cr, uid, session_id, context=context)
        if s.state == 'opened':
            return self.open_ui(cr, uid, ids, context=context)
        return self._open_session(session_id)

    def open_existing_session_cb_close(self, cr, uid, ids, context=None):
        ps_obj = self.pool['pos.session']
        session_ids = ps_obj.search(
            cr, uid, [('state', '=', 'closing_control')])
        if len(session_ids) > 1:
            return {
                'name': _('Session'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'pos.session',
                'domain': [('state', '=', 'closing_control')],
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
        else:
            wf_service = netsvc.LocalService('workflow')
            wizard = self.browse(cr, uid, ids[0], context=context)
            wf_service.trg_validate(
                uid, 'pos.session', wizard.pos_session_id.id,
                'cashbox_control', cr)
            return self.open_session_cb(cr, uid, ids, context)

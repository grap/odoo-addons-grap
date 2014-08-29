# -*- encoding: utf-8 -*-
##############################################################################
#
#    Pos Invoicing module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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


class pos_invoice_draft_order(TransientModel):
    _name = 'pos.invoice.draft.order'

    # Action section
    def invoice_draft_order(self, cr, uid, ids, context=None):
        if context is None:
            return False
        order_id = context.get('active_id', False)
        if not order_id:
            return False

        po_obj = self.pool.get('pos.order')
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'pos.order', order_id, 'paid', cr)
        res = po_obj.action_invoice(cr, uid, [order_id], context=context)
        return res

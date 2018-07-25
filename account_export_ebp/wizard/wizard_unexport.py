# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv
import logging
_logger = logging.getLogger(__name__)


class account_unexport_ebp(osv.TransientModel):
    _name = "account.unexport.ebp"

    # Columns Section
    _columns = {
    }

    def unexport(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        unexport_ids = context.get('active_ids', False)
        am_obj = self.pool.get('account.move')
        am_obj.write(cr, uid, unexport_ids, {
            'exported_ebp_id': False,
        }, context=context)
        # TODO: find the file in ebp.export model and remove the move lines
        return ids

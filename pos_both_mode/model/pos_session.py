# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Both Mode module for Odoo
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

from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class pos_session(Model):
    _inherit = 'pos.session'

    def open_cb_backend(self, cr, uid, ids, context=None):
        if context is None:
            context = dict()

        context['search_default_Today'] = 1

        if isinstance(ids, (int, long)):
            ids = [ids]

        this_record = self.browse(cr, uid, ids[0], context=context)
        this_record._workflow_signal('open')

        context.update(active_id=this_record.id)
        return {
            'name': _("Orders"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'target': 'current',
            'view_id': False,
            'context': context,
        }

    def open_frontend_cb_backend(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        context['search_default_Today'] = 1
        if not ids:
            return {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.user_id.id != uid:
                raise osv.except_osv(_('Error!'), _(
                    """You cannot use the  session of another users. This"""
                    """ session is owned by %s. Please first close this one"""
                    """ to use this point of sale""" % session.user_id.name))
        context.update({'active_id': ids[0]})
        return {
            'name': _("Orders"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'target': 'current',
            'view_id': False,
            'context': context,
        }

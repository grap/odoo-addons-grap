# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_move(osv.osv):
    _inherit = "account.move"

    # Columns section
    def _export_name(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for move in self.browse(cr, uid, ids, context=context):
                result[move.id] = move.exported_ebp_id\
                    and 'export_' + str(move.exported_ebp_id.id) or ''
        return result

    _columns = {
        'exported_ebp_id': fields.many2one(
            'ebp.export', 'Transfer id',
            help="""Indicates whether the move has already been exported"""
            """ to EBP or not. It is changed automatically."""),
        'exported_ebp': fields.function(
            _export_name, type='char', string='export id', store=False),
    }

    # Override section
    def write(self, cr, uid, ids, vals, context=None):
        """Refuse to change changes exported Moves"""
        if 'exported_ebp_id' not in vals:
            exported_move_ids = self.search(
                cr, uid, [('exported_ebp_id', '!=', False), ('id', 'in', ids)])
            if exported_move_ids:
                exported_moves = self.browse(
                    cr, uid, exported_move_ids, context=context)
                raise osv.except_osv(
                    _('Exported move!'),
                    _('You cannot modify exported moves: %s!')
                    % ', '.join([m.name for m in exported_moves]))
        return super(osv.osv, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context=None, check=True):
        """Refuse to delete exported Moves"""
        exported_move_ids = self.search(
            cr, uid, [('exported_ebp_id', '!=', False), ('id', 'in', ids)])
        if exported_move_ids:
            exported_moves = self.browse(
                cr, uid, exported_move_ids, context=context)
            raise osv.except_osv(
                _('Exported move!'),
                _('You cannot delete exported moves: %s!')
                % ', '.join([m.name for m in exported_moves]))
        return super(account_move, self).unlink(cr, uid, ids, context)

    def copy(self, cr, uid, pId, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'exported_ebp_id': False,
        })
        return super(account_move, self).copy(
            cr, uid, pId, default, context=context)

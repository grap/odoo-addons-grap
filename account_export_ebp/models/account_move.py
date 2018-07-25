# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

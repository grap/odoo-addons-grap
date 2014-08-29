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

from openerp.osv import fields
from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


# TODO: this can be removed once all sessions
# with sale journal sales are closed
class pos_config(Model):
    _inherit = 'pos.config'

    _columns = {
        'journal_ids': fields.many2many(
            'account.journal', 'pos_config_journal_rel',
            'pos_config_id', 'journal_id', 'Available Payment Methods',
            domain=(
                """[('journal_user', '=', True ),"""
                """ ('type', 'in', ['bank', 'cash', 'sale'])]"""),),
    }


# TODO: this can be removed once all sessions with sale journal sales
# are closed
class pos_session(Model):
    _inherit = 'pos.session'

    def wkf_action_close(self, cr, uid, ids, context=None):
        # Close CashBox
        bsl = self.pool.get('account.bank.statement.line')
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if st.state == 'confirm':
                    continue
                if abs(st.difference) > st.journal_id.amount_authorized_diff:
                    # The pos manager can close statements with maximums.
                    if not self.pool.get('ir.model.access').check_groups(
                            cr, uid, "point_of_sale.group_pos_manager"):
                        raise osv.except_osv(_('Error!'), _(
                            """Your ending balance is too different from"""
                            """ the theoretical cash closing (%.2f), the"""
                            """ maximum allowed is: %.2f. You can contact"""
                            """ your manager to force it.""") % (
                                st.difference,
                                st.journal_id.amount_authorized_diff))
                if (st.journal_id.type not in ['bank', 'cash', 'sale']):
                    raise osv.except_osv(_('Error!'), _(
                        """The type of the journal for your payment method"""
                        """ should be bank or cash """))
                if st.difference and st.journal_id.cash_control is True:
                    if st.difference > 0.0:
                        name = _('Point of Sale Profit')
                        account_id = st.journal_id.profit_account_id.id
                    else:
                        account_id = st.journal_id.loss_account_id.id
                        name = _('Point of Sale Loss')
                    if not account_id:
                        raise osv.except_osv(_('Error!'), _(
                            """Please set your profit and loss accounts on"""
                            """ your payment method '%s'. This will allow"""
                            """ OpenERP to post the difference of %.2f in"""
                            """ your ending balance. To close this session,"""
                            """ you can update the 'Closing Cash Control' to"""
                            """ avoid any difference.""") % (
                                st.journal_id.name, st.difference))
                    bsl.create(cr, uid, {
                        'statement_id': st.id,
                        'amount': st.difference,
                        'ref': record.name,
                        'name': name,
                        'account_id': account_id
                    }, context=context)

                if st.journal_id.type == 'bank':
                    st.write({'balance_end_real': st.balance_end})
                if st.journal_id.type != 'sale':
                    getattr(st, 'button_confirm_%s' % st.journal_id.type)(
                        context=context)
        self._confirm_orders(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'closed'}, context=context)

        obj = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'point_of_sale', 'menu_point_root')[1]
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Sale Menu',
            'tag': 'reload',
            'params': {'menu_id': obj},
        }


class pos_order(Model):
    _inherit = 'pos.order'

    def action_invoice(self, cr, uid, ids, context=None):
        for po in self.browse(cr, uid, ids, context=context):
            if po.state not in ('draft', 'paid'):
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not invoice a non new or non paid POS Order"))
            if po.state == 'draft' and len(po.statement_ids) != 0:
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not invoice a partial paid POS Order"))
        res = super(pos_order, self).action_invoice(
            cr, uid, ids, context=context)
        if context and context.get('forbid_payment', False):
            invoice_id = res.get('res_id', False)
            if invoice_id:
                inv_obj = self.pool.get('account.invoice')
                inv = inv_obj.browse(cr, uid, invoice_id, context=context)
                inv.write({'forbid_payment': True})
                inv_obj.action_date_assign(cr, uid, [invoice_id])
                inv.action_move_create(context=context)
                inv.action_number(context=context)
                inv.invoice_validate(context=context)
        return res

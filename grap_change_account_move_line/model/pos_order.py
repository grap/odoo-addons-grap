# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Account Move Lines Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
# flake8: noqa

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class pos_order(osv.osv):
    _inherit = 'pos.order'

    def compute_tax(self, cr, uid, amount, tax, line, context=None):
        if amount > 0:
            tax_code_id = tax['base_code_id']
            tax_amount = line.price_subtotal * tax['base_sign']
        else:
            tax_code_id = tax['ref_base_code_id']
            tax_amount = line.price_subtotal * tax['ref_base_sign']

        return (tax_code_id, tax_amount,)

    def compute_group_tax(
            self, cr, uid, cur, line, group_tax, current_company,
            context=None):
        account_tax_obj = self.pool['account.tax']
        cur_obj = self.pool['res.currency']

        taxes = []
        for ptri in line.pol_tax_rel_id:
            if ptri.tax_id.company_id.id == current_company.id:
                taxes.append(ptri.tax_id)

        computed_taxes = account_tax_obj.compute_all(
            cr, uid, taxes, line.price_unit * (100.0 - line.discount) / 100.0,
            line.qty)['taxes']

        tax_amount = 0
        for tax in computed_taxes:
            tax_amount += cur_obj.round(cr, uid, cur, tax['amount'])
            group_key = self._get_tax_key(cr, uid, tax, context=context)
            group_tax.setdefault(group_key, 0)
            group_tax[group_key] += cur_obj.round(cr, uid, cur, tax['amount'])
        return (computed_taxes, group_tax, tax_amount)

    def _get_key(self, cr, uid, data_type, values, context=None):
        key = False
        if data_type == 'product':
            key = (
                'product', values['tax_code_id'], values['account_id'],
                values['debit'] > 0)
            values.update({'name': _('Various Products')})
        elif data_type == 'tax':
            key = ('tax', values['tax_code_id'], values['debit'] > 0)
        elif data_type == 'counter_part':
            key = ('counter_part', values['account_id'], values['debit'] > 0)
        return key

    def _get_tax_key(self, cr, uid, tax, context=None):
        return (
            tax['tax_code_id'],
            tax['base_code_id'],
            tax['account_collected_id'],
            tax['id'],
            )

    def insert_data(self, cr, uid, data_type, values, grouped_data,
                                                have_to_group_by, context=None):
        key = self._get_key(cr, uid, data_type, values)
        if not key:
            return
        grouped_data.setdefault(key, [])

        if have_to_group_by:
            if not grouped_data[key]:
                grouped_data[key].append(values.copy())
            else:
                current_value = grouped_data[key][0]
                current_value['quantity'] = current_value.get(
                                'quantity', 0.0) + values.get('quantity', 0.0)
                current_value['credit'] = current_value.get(
                                    'credit', 0.0) + values.get('credit', 0.0)
                current_value['debit'] = current_value.get(
                                        'debit', 0.0) + values.get('debit', 0.0)
                current_value['tax_amount'] = current_value.get('tax_amount',
                                            0.0) + values.get('tax_amount', 0.0)
        else:
            grouped_data[key].append(values.copy())
            
    def _create_account_move_line(self, cr, uid, ids, session=None,
                                                    move_id=None, context=None):
        # Tricky, via the workflow, we only have one id in the ids variable
        """Create a account move line of order grouped by products or not."""
        account_move_obj = self.pool.get('account.move')
        account_period_obj = self.pool.get('account.period')
        property_obj = self.pool.get('ir.property')
        account_journal_obj = self.pool.get('account.journal')

        if session and not all(
            session.id == order.session_id.id for order in self.browse(
                                                cr, uid, ids, context=context)
            ):
            raise osv.except_osv(_('Error!'),
                            _('Selected orders do not have the same session!'))

        grouped_data = {}
        have_to_group_by = session and session.config_id.group_by or False

        move_ids = []

        for order in self.browse(cr, uid, ids, context=context):
            if order.account_move:
                continue
            if order.state != 'paid':
                continue

            current_company = order.sale_journal.company_id
            group_tax = {}
            account_def = property_obj.get(cr, uid,
                'property_account_receivable', 'res.partner', context=context)

            order_account = order.partner_id and \
                            order.partner_id.property_account_receivable and \
                            order.partner_id.property_account_receivable.id or \
                            account_def and account_def.id or \
                            current_company.account_receivable.id
            if not order_account:
                    raise osv.except_osv(_('Error!'),
                                            _('No account_receivable found.'))
            
            ctx = dict(context or {}, company_id=current_company.id,
                                        account_period_prefer_normal=True)
            if account_journal_obj.browse(cr, uid, order.sale_journal.id, context=context).allow_date:
                period_id = account_period_obj.find(cr, uid,
                    dt=order.date_order[:10], context=ctx)[0]
            else:
                period_id = account_period_obj.find(cr, uid, context=ctx)[0]

            if move_id is None:
                # Create an entry for the sale
                move_id = account_move_obj.create(cr, uid, {
                    'date': order.date_order[:10],
                    'period_id' : period_id,
                    'ref' : order.name,
                    'journal_id': order.sale_journal.id,
                }, context=context)

            move_ids.append(move_id)

            #because of the weird way the pos order is written, we need to make sure there is at least one line, 
            #because just after the 'for' loop there are references to 'line' and 'income_account' variables (that 
            #are set inside the for loop)
            #TOFIX: a deep refactoring of this method (and class!) is needed in order to get rid of this stupid hack
            assert order.lines, _('The POS order must have lines when calling this method')
            # Create an move for each order line

            cur = order.pricelist_id.currency_id
            for line in order.lines:
                (computed_taxes,
                group_tax,
                tax_amount,) = self.compute_group_tax(cr, uid, cur, line, 
                                    group_tax, current_company, context=context)

                amount = line.price_subtotal

                # Search for the income account
                if line.product_id.property_account_income.id:
                    income_account = line.product_id.property_account_income.id
                elif line.product_id.categ_id.property_account_income_categ.id:
                    income_account = line.product_id.categ_id\
                                        .property_account_income_categ.id
                else:
                    raise osv.except_osv(_('Error!'), _('Please define income '\
                        'account for this product: "%s" (id:%d).') \
                        % (line.product_id.name, line.product_id.id, ))

                # Empty the tax list as long as there is no tax code:
                tax_code_id = False
                while computed_taxes:
                    tax = computed_taxes.pop(0)
                    tax_code_id, tax_amount = self.compute_tax(cr, uid,
                                                            amount, tax, line)

                    # If there is one we stop
                    if tax_code_id:
                        break
                
                common_values = {
                    'company_id': current_company,
                    'journal_id' : order.sale_journal.id,
                    'period_id' : period_id,
                    'date': order.date_order[:10],
                    'ref': order.name,
                    'move_id' : move_id,
                    'partner_id': order.partner_id and\
                        self.pool.get("res.partner")._find_accounting_partner(
                        order.partner_id).id or False
                    
                    }
                # Create a move for the line
                values = common_values
                values.update({
                    'name': line.product_id.name,
                    'quantity': line.qty,
                    'product_id': line.product_id.id,
                    'account_id': income_account,
                    'credit': ((amount>0) and amount) or 0.0,
                    'debit': ((amount<0) and -amount) or 0.0,
                    'tax_code_id': tax_code_id,
                    'tax_amount': tax_amount,
                    })
                self.insert_data(cr, uid, 'product', values,
                                                grouped_data, have_to_group_by)

                # For each remaining tax with a code, whe create a move line
                for tax in computed_taxes:
                    tax_code_id, tax_amount = self.compute_tax(cr, uid, amount,
                                                                    tax, line)
                    if not tax_code_id:
                        continue

                    values = common_values
                    values.update({
                        'name': line.product_id.name,
                        'quantity': line.qty,
                        'product_id': line.product_id.id,
                        'account_id': income_account,
                        'credit': ((amount>0) and amount) or 0.0,
                        'debit': ((amount<0) and -amount) or 0.0,
                        'tax_code_id': tax_code_id,
                        'tax_amount': tax_amount,
                        })
                    self.insert_data(cr, uid, 'tax', values,
                                                grouped_data, have_to_group_by)

            # Create a move for each tax group
            (tax_code_pos, base_code_pos, account_pos, tax_id)= (0, 1, 2, 3)

            for key, tax_amount in group_tax.items():
                tax = self.pool.get('account.tax').browse(cr, uid, key[tax_id],
                                                                context=context)
                values = common_values
                values.update({
                    'name': _('Tax') + ' ' + tax.name,
                    'quantity': line.qty,
                    'product_id': line.product_id.id,
                    'account_id': key[account_pos] or income_account,
                    'credit': ((tax_amount>0) and tax_amount) or 0.0,
                    'debit': ((tax_amount<0) and -tax_amount) or 0.0,
                    'tax_code_id': key[tax_code_pos],
                    'tax_amount': tax_amount,
                    })
                self.insert_data(cr, uid, 'tax', values, grouped_data,
                                                            have_to_group_by)

            # counterpart
            values = common_values
            values.update({
                'name': _("Trade Receivables"), #order.name,
                'account_id': order_account,
                'credit': ((order.amount_total < 0) and\
                    -order.amount_total) or 0.0,
                'debit': ((order.amount_total > 0) and\
                    order.amount_total) or 0.0,
                })
            self.insert_data(cr, uid, 'counter_part', values, grouped_data,
                                                            have_to_group_by)

            order.write({'state':'done', 'account_move': move_id})

        all_lines = []
        for group_key, group_data in grouped_data.iteritems():
            for value in group_data:
                all_lines.append((0, 0, value),)
        if move_id: #In case no order was changed
            self.pool.get("account.move").write(cr, uid, [move_id],
                                        {'line_id':all_lines}, context=context)
            try:
                self.pool.get("account.move").post(cr, uid, [move_id],
                                                                context=context)
            except:
                # TODO: write a logger
                # print "Impossible to validate the move (id=%s)" % move_id
                pass
        return move_ids

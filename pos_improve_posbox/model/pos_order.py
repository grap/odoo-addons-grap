# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - PosBox Improvements module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from datetime import datetime

from openerp.osv import fields
from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class pos_order(Model):
    _inherit = 'pos.order'

    _columns = {
        'iface_print_via_proxy': fields.related(
            'session_id', 'config_id', 'iface_print_via_proxy', type='boolean',
            string='Print via Proxy'),
    }

    def print_receipt_posbox(self, cr, uid, ids, context=None):
        if isinstance(ids, list):
            if len(ids) != 1:
                raise osv.except_osv(
                    _('Error!'), _('Please select one Pos Order.'))
        else:
            ids = [ids]
        context = context or {}
        receipt = self.get_export_receipt(cr, uid, ids[0])
        po = self.browse(cr, uid, ids[0], context=context)
        ctx = context.copy()
        ctx['receipt'] = receipt
        ctx['url'] = po.session_id.config_id.proxy_ip
        ctx['timeout'] = po.session_id.config_id.proxy_timeout
        return {
            'type': 'ir.actions.client',
            'name': _('Print Quick Direct'),
            'tag': 'pos.posbox',
            'target': 'new',
            'context': ctx,
        }

    def get_export_receipt(self, cr, uid, pId, context=None):
        """Generate a structure with pos order datas, compatible with
            PosBox webServices. Function overloadable."""
        receipt = {}
        po = self.browse(cr, uid, pId, context=context)

        # Orderlines part
        orderlines = []
        for line in po.lines:
            orderlines.append({
                'quantity': line.qty,
                'unit_name': line.product_id.uom_id.name,
                'price': line.price_unit,
                'discount': line.discount,
                'product_name': line.product_id.name,
                'price_display': line.price_subtotal_incl,
                'price_with_tax': line.price_subtotal_incl,
                'price_without_tax': line.price_subtotal_incl,
                'tax': line.price_subtotal_incl - line.price_subtotal,
                'product_description': line.product_id.description,
                'product_description_sale': line.product_id.description_sale,
            })
        receipt['orderlines'] = orderlines

        # Paymentlines part
        paymentlines = []
        change_lines = []

        # recompute if possible the ???
        change_line_id = 0
        change_line_amount = 0
        for statement_id in po.statement_ids:
            if statement_id.journal_id.type == 'cash'\
                    and statement_id.amount < 0:
                change_lines.append(statement_id)
        if len(change_lines) == 1:
            change_line_id = change_lines[0].id
            change_line_amount = change_lines[0].amount

        for statement_id in po.statement_ids:
            if statement_id.id != change_line_id:
                paymentlines.append({
                    'amount': statement_id.amount,
                    'journal': statement_id.journal_id.name,
                })
        receipt['paymentlines'] = paymentlines

        # Global part
        receipt['subtotal'] = po.amount_total - po.amount_tax
        receipt['total_with_tax'] = po.amount_total
        receipt['total_without_tax'] = po.amount_total - po.amount_tax
        receipt['total_tax'] = po.amount_tax
        receipt['total_paid'] = po.amount_total
        # Set to 0 total_discount because the value is bad managed by default
        # (there is a tax problem with exclude tax)
        receipt['total_discount'] = 0
        receipt['change'] = - change_line_amount
        receipt['name'] = po.name
        receipt['client'] = po.partner_id.name
        receipt['invoice_id'] = po.invoice_id.name if po.invoice_id else None
        receipt['cashier'] = po.user_id.name
        dt = datetime.strptime(po.date_order, '%Y-%m-%d %H:%M:%S')
        receipt['date'] = {
            'year': dt.year,
            'month': dt.month - 1,
            'date': dt.day,
            'day': dt.weekday(),
            'hour': dt.hour,
            'minute': dt.minute,
        }
        receipt['company'] = {
            'email': po.company_id.email,
            'website': po.company_id.website,
            'company_registry': '',
            'contact_address': po.company_id.partner_id.contact_address,
            'vat': po.company_id.vat,
            'name': po.company_id.name,
            'phone': po.company_id.phone,
        }
        receipt['shop'] = {
            'name': po.shop_id.name,
        }
        receipt['currency'] = po.pricelist_id.currency_id.symbol
        return receipt

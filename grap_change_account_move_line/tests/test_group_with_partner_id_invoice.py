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

from openerp import netsvc
from openerp.tests.common import TransactionCase


class TestGroupWithPartnerInvoiceId(TransactionCase):

    def setUp(self):
        super(TestGroupWithPartnerInvoiceId, self).setUp()
        cr, uid = self.cr, self.uid
        self.imd_obj = self.registry('ir.model.data')
        self.imm_obj = self.registry('ir.module.module')
        self.ps_obj = self.registry('pos.session')
        self.pp_obj = self.registry('product.product')
        self.po_obj = self.registry('pos.order')
        self.pol_obj = self.registry('pos.order.line')
        self.at_obj = self.registry('account.tax')
        self.am_obj = self.registry('account.move')
        self.pmp_obj = self.registry('pos.make.payment')
        self.abs_obj = self.registry('account.bank.statement')
        self.wf_service = netsvc.LocalService('workflow')
        self.customer_partner_id = self.imd_obj.get_object_reference(
            cr, uid, 'base', 'res_partner_3')[1]
        self.product_1 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_48')[1]
        self.pos_config_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        self.cash_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'cash_journal')[1]
        self.sale_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'sales_journal')[1]

    # Test Section
    def test_01_group_by_partner_with_without(self):
        """[Functional Test] Test if 1 PO with partner and 1 PO invoice
        correct entries. (1 sale and 2 cash)."""
        cr, uid = self.cr, self.uid

        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])

        # Create Order #1. Paid with Customer
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
            'partner_id': self.customer_partner_id,
            'lines': [[0, 0, {
                'product_id': self.product_1,
                'discount': 0, 'qty': 1,
                'price_unit': 111}]]
        })

        # Make Payment Order #1
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 111,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})

        # Create Order #2. Paid with Customer AND Invoice
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
            'partner_id': self.customer_partner_id,
            'lines': [[0, 0, {
                'product_id': self.product_1,
                'discount': 0, 'qty': 1,
                'price_unit': 222}]]
        })
        # Make Payment Order #2
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 222,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})
        self.po_obj.action_invoice(cr, uid, [po_id])

        # Close Session
        abs_id = self.abs_obj.search(cr, uid, [
            ('journal_id', '=', self.cash_journal_id)], order='id DESC')[0]
        self.abs_obj.write(cr, uid, [abs_id], {
            'details_ids': [[0, False, {
                'pieces': 333,
                'number_closing': 1}]]})
        self.wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'cashbox_control', cr)
        self.wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'close', cr)

        cr.commit()  # FIXME

        # Check Sale Move Without customer
        ps = self.ps_obj.browse(cr, uid, ps_id)
        sale_move_ids = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id),
            ('partner_id', '=', False)])
        sale_move = self.am_obj.browse(cr, uid, sale_move_ids[0])
        credit = debit = 0
        for line in sale_move.line_id:
            credit += line.credit
            debit += line.debit

        self.assertEquals(
            credit, debit,
            """Validate POS session must created balanced Sale Move.""")
        self.assertEquals(
            len(sale_move_ids), 1,
            """Validate 1 Order with customer and 1 Order Invoiced
            must create 1 Sale Entry Without customer.""")
        self.assertEquals(
            credit, 111,
            """Validate 1 Order with customer and 1 Order Invoice
            must create an entry with sale of the first Order.""")

        ps = self.ps_obj.browse(cr, uid, ps_id)
        # Check Sale Move With customer
        sale_move_ids = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id),
            ('partner_id', '=', self.customer_partner_id)])

        self.assertEquals(
            len(sale_move_ids), 0,
            """Validate 1 Order with customer and 1 Order Invoiced
            must not create 1 Sale Entry With customer but an invoice""")

        # Check Cash Move
        cash_move_ids = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.cash_journal_id),
            ('partner_id', '=', False)])
        cash_move = self.am_obj.browse(cr, uid, cash_move_ids[0])
        credit = debit = 0
        for line in cash_move.line_id:
            credit += line.credit
            debit += line.debit

        self.assertEquals(
            credit, debit,
            """Validate POS session must created balanced Cash Move.""")
        self.assertEquals(
            len(cash_move_ids), 1,
            """Validate 1 Order with customer and 1 Order Invoiced
            must create 1 Sale Entry Without customer.""")
        self.assertEquals(
            credit, 111,
            """Validate 1 Order with customer and 1 Order Invoice
            must create an entry with Cash of the first Order.""")

        # Check Cash Move (With partner)
        cash_move_ids = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.cash_journal_id),
            ('partner_id', '=', self.customer_partner_id)])
        cash_move = self.am_obj.browse(cr, uid, cash_move_ids[0])
        credit = debit = 0
        for line in cash_move.line_id:
            credit += line.credit
            debit += line.debit

        self.assertEquals(
            credit, debit,
            """Validate POS session must created balanced Cash Move.""")
        self.assertEquals(
            len(cash_move_ids), 1,
            """Validate 1 Order with customer and 1 Order Invoiced
            must create 1 Sale Entry Without customer.""")
        self.assertEquals(
            credit, 222,
            """Validate 1 Order with customer and 1 Order Invoice
            must create an entry with Cash of the first Order.""")

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Group Move Line Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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


class TestAccountGroupMoveLines(TransactionCase):

    def setUp(self):
        super(TestAccountGroupMoveLines, self).setUp()
        cr, uid = self.cr, self.uid
        self.imd_obj = self.registry('ir.model.data')
        self.ai_obj = self.registry('account.invoice')
        self.aj_obj = self.registry('account.journal')
        self.ail_obj = self.registry('account.invoice.line')
        self.am_obj = self.registry('account.move')
        self.ps_obj = self.registry('pos.session')
        self.po_obj = self.registry('pos.order')
        self.pol_obj = self.registry('pos.order.line')
        self.pmp_obj = self.registry('pos.make.payment')
        self.pp_obj = self.registry('product.product')
        self.sale_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'sales_journal')[1]
        self.customer_partner_id = self.imd_obj.get_object_reference(
            cr, uid, 'base', 'res_partner_2')[1]
        self.customer_account_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_recv')[1]
        self.account_sale_1 = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_sale')[1]
        self.account_sale_2 = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'income_fx_income')[1]
        self.product_1 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_48')[1]
        self.product_2 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_24')[1]
        self.product_3 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_16')[1]
        self.product_4 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_35')[1]
        self.pos_config_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        self.cash_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'cash_journal')[1]

    # Test Section
    def test_01_generate_move_from_invoice(self):
        """[Functional Test] Create Customer Invoice and check correct
        generated moves"""
        cr, uid = self.cr, self.uid
        # Set Journal to group invoice lines
        self.aj_obj.write(cr, uid, self.sale_journal_id, {
            'group_invoice_lines': True,
        })

        ai_id = self.ai_obj.create(cr, uid, {
            'partner_id': self.customer_partner_id,
            'account_id': self.customer_account_id,
        })
        # Line 1 : Product 1 - account 1
        self.ail_obj.create(cr, uid, {
            'product_id': self.product_1,
            'invoice_id': ai_id,
            'name': 'Account 1 - price : 2',
            'account_id': self.account_sale_1,
            'price_unit': 2,
        })
        # Line 2 : Product 2 - account 1
        self.ail_obj.create(cr, uid, {
            'product_id': self.product_2,
            'invoice_id': ai_id,
            'name': 'Account 1 - price : 30',
            'account_id': self.account_sale_1,
            'price_unit': 30,
        })
        # Line 3 : Product 3 - account 2
        self.ail_obj.create(cr, uid, {
            'product_id': self.product_3,
            'invoice_id': ai_id,
            'name': 'Account 2 - price : 2',
            'account_id': self.account_sale_2,
            'price_unit': 4,
        })
        # Line 4 : Product 4 - account 2
        self.ail_obj.create(cr, uid, {
            'product_id': self.product_4,
            'invoice_id': ai_id,
            'name': 'Account 2 - price : 30',
            'account_id': self.account_sale_2,
            'price_unit': 50,
        })

        wf_service = netsvc.LocalService('workflow')
        wf_service.trg_validate(
            uid, 'account.invoice', ai_id, 'invoice_open', cr)

        ai = self.ai_obj.browse(cr, uid, ai_id)
        self.assertEquals(
            len(ai.move_id.line_id), 3,
            """Validate customer invoices with 2 distincts sale accounts"""
            """ must generate a move with 3 lines""")
        line_account_1 = False
        line_account_2 = False
        for line in ai.move_id.line_id:
            if line.account_id.id == self.account_sale_1:
                line_account_1 = line
            if line.account_id.id == self.account_sale_2:
                line_account_2 = line

        self.assertNotEquals(
            line_account_1, False,
            """Validate Customer invoices with Sale Account #1 must generate"""
            """ one single move line with account #1.""")
        self.assertNotEquals(
            line_account_2, False,
            """Validate Customer invoices with Sale Account #2 must generate"""
            """ one single move line with account #2.""")

        self.assertEquals(
            line_account_1.credit, 2 + 30,
            """Validate Customer invoices with Sale Account #1 lines"""
            """ must generate one single move line width summed value.""")
        self.assertEquals(
            line_account_2.credit, 4 + 50,
            """Validate Customer invoices with Sale Account #2 lines"""
            """ must generate one single move line width summed value.""")

    # Test Section
    def test_02_generate_move_from_point_of_sale(self):
        """[Functional Test] Create Multiple POS order and check correct
        generated moves"""
        cr, uid = self.cr, self.uid
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])

        # Set account Products for test
        self.pp_obj.write(cr, uid, [self.product_1, self.product_2], {
            'property_account_income': self.account_sale_1,
        })
        self.pp_obj.write(cr, uid, [self.product_3, self.product_4], {
            'property_account_income': self.account_sale_2,
        })

        # Create Order #1
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
        })
        # PO1 - Line 1 : Product 1 - account 1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_1,
            'name': 'Product 1 - Account 1',
            'price_unit': 2,
        })
        # PO1 - Line 2 : Product 3 - account 2
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_3,
            'name': 'Product 3 - Account 2',
            'price_unit': 4,
        })
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 6,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})
        # Create Order #2
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
        })
        # PO2 - Line 1 : Product 2 - account 1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_2,
            'name': 'Product 2 - Account 1',
            'price_unit': 30,
        })
        # PO2 - Line 2 : Product 4 - account 2
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_4,
            'name': 'Product 4 - Account 2',
            'price_unit': 50,
        })
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 80,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})

        # Create Order #3
        po_id = self.po_obj.create(cr, uid, {
            'partner_id': self.customer_partner_id,
            'session_id': ps_id,
        })
        # PO3 - Line 1 : Product 1 - account 1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_1,
            'name': 'Product 1 - Account 1',
            'price_unit': 2000,
        })
        # PO3 - Line 2 : Product 3 - account 2
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_3,
            'name': 'Product 3 - Account 2',
            'price_unit': 4000,
        })
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 6000,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})
        # Create Order #4
        po_id = self.po_obj.create(cr, uid, {
            'partner_id': self.customer_partner_id,
            'session_id': ps_id,
        })
        # PO4 - Line 1 : Product 2 - account 1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_2,
            'name': 'Product 2 - Account 1',
            'price_unit': 30000,
        })
        # PO4 - Line 2 : Product 4 - account 2
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_4,
            'name': 'Product 4 - Account 2',
            'price_unit': 50000,
        })
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 80000,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})

        # Close Session
        wf_service = netsvc.LocalService('workflow')
        wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'close', cr)

        ps = self.ps_obj.browse(cr, uid, ps_id)

        # Check Sale Move Without Customer
        sale_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id),
            ('partner_id', '=', False)])

        self.assertEquals(
            len(sale_move_id), 1,
            """Validate POS Session must create one Sale Move w/o Customer""")
        sale_move_without = self.am_obj.browse(cr, uid, sale_move_id[0])

        line_account_1 = False
        line_account_2 = False
        for line in sale_move_without.line_id:
            if line.account_id.id == self.account_sale_1:
                line_account_1 = line
            if line.account_id.id == self.account_sale_2:
                line_account_2 = line

        self.assertNotEquals(
            line_account_1, False,
            """Validate POS sesion invoices must generate"""
            """ one single Sale move line with account #1.""")
        self.assertNotEquals(
            line_account_2, False,
            """Validate POS sesion invoices must generate"""
            """ one single Sale move line with account #2.""")

        self.assertEquals(
            line_account_1.credit, 2 + 30,
            """Validate POS Session with Sale Account #1"""
            """ must generate one single move line with summed value.""")
        self.assertEquals(
            line_account_2.credit, 4 + 50,
            """Validate POS Session with Sale Account #1"""
            """ must generate one single move line with summed value.""")

        # Check Sale Move with Customer
        sale_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id),
            ('partner_id', '=', self.customer_partner_id)])
        self.assertEquals(
            len(sale_move_id), 1,
            """Validate POS Session must create one Sale Move by Customer""")

        # Check Cash Move without Customer
        cash_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.cash_journal_id),
            ('partner_id', '=', False)])

        self.assertEquals(
            len(cash_move_id), 1,
            """Validate POS Session must create one Cash Move w/o Customer""")

        # Check Cash Move with Customer
        cash_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.cash_journal_id),
            ('partner_id', '=', self.customer_partner_id)])
        self.assertEquals(
            len(cash_move_id), 1,
            """Validate POS Session must create one Cash Move by Customer""")

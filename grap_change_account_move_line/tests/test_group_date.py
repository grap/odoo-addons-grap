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


class TestGroupMoveLine(TransactionCase):

    def setUp(self):
        super(TestGroupMoveLine, self).setUp()
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
        self.abs_obj = self.registry('account.bank.statement')
        self.acl_obj = self.registry('account.cashbox.line')
        self.imm_obj = self.registry('ir.module.module')
        self.wf_service = netsvc.LocalService('workflow')
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
            cr, uid, 'grap_change_account_move_line', 'product_1_account_1')[1]
        self.product_2 = self.imd_obj.get_object_reference(
            cr, uid, 'grap_change_account_move_line', 'product_2_account_1')[1]
        self.product_3 = self.imd_obj.get_object_reference(
            cr, uid, 'grap_change_account_move_line', 'product_3_account_2')[1]
        self.product_4 = self.imd_obj.get_object_reference(
            cr, uid, 'grap_change_account_move_line', 'product_4_account_2')[1]
        self.pos_config_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        self.cash_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'cash_journal')[1]

    # Test Section
    def test_01_generate_with_multiple_date(self):
        """[Functional Test] Create Customer Invoice and check correct
        generated moves"""
        cr, uid = self.cr, self.uid
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
            'start_at': '01/01/2015 01:01:01',
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])

        # Create Order #1
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
            'date_order': '02/01/2015 02:02:02',
        })
        # PO1 - Line 1 : Product 1 - account 1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_1,
            'name': 'Product 1 - Account 1',
            'price_unit': 30,
        })
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 30,
             'payment_date' : '03/01/2015 03:03:03',
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})

        # Close Session
        abs_id = self.abs_obj.search(cr, uid, [
            ('journal_id', '=', self.cash_journal_id)], order='id DESC')[0]
        self.abs_obj.write(cr, uid, [abs_id], {
            'details_ids': [[0, False, {
                'pieces': 30,
                'number_closing': 1}]]})
        self.wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'cashbox_control', cr)
        self.wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'close', cr)

        ps = self.ps_obj.browse(cr, uid, ps_id)

        # Check Sale Move Date
        sale_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id)])

        sale_move = self.am_obj.browse(cr, uid, sale_move_id[0])

        self.assertEquals(
            sale_move.date, ps.stop_at[:10],
            """The sale move must have the stop date of the session.""")

        # Check Sale Move Date
        cash_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.cash_journal_id)])

        cash_move = self.am_obj.browse(cr, uid, cash_move_id[0])

        self.assertEquals(
            cash_move.date, ps.stop_at[:10],
            """The cash move must have the stop date of the session.""")

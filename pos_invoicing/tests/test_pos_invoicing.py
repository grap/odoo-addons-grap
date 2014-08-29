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

import time
from openerp import netsvc
from openerp.tests.common import TransactionCase


class TestPosInvoicing(TransactionCase):
    """Tests for POS Invoicing Module"""

    def setUp(self):
        super(TestPosInvoicing, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.abs_obj = self.registry('account.bank.statement')
        self.pp_obj = self.registry('product.product')
        self.pc_obj = self.registry('pos.config')
        self.ps_obj = self.registry('pos.session')
        self.po_obj = self.registry('pos.order')
        self.wf_service = netsvc.LocalService("workflow")

    # Test Section
    def test_01_invoice_payment_now(self):
        """Test the workflow order -> payment -> invoice"""
        cr, uid = self.cr, self.uid
        # Getting object
        pc_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        rp_c2c_id = self.imd_obj.get_object_reference(
            cr, uid, 'base', 'res_partner_12')[1]
        pp_usb_id = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_48')[1]
        aj_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'cash_journal')[1]
        # Opening Session
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': pc_id,
            })
        # create Pos Order
        po_id = self.po_obj.create(cr, uid, {
            'partner_id': rp_c2c_id,
            'lines': [[0, False, {
                'product_id': pp_usb_id,
                'qty': 100,
                'price_unit': 10,
            }]],
            })
        # Realize Partial Payment
        self.po_obj.add_payment(cr, uid, po_id, {
            'journal': aj_id,
            'payment_date': time.strftime('%Y-%m-%d'),
            'amount': 500,
        })
        # Sub Test 1 : Try Invoice : Must Fail
        error = False
        try:
            self.po_obj.action_invoice(cr, uid, [po_id])
        except:
            error = True
        self.assertEquals(
            error, True, "A partial paid Pos Order can Not be invoiced!")

        # Finish Payment
        self.po_obj.add_payment(cr, uid, po_id, {
            'journal': aj_id,
            'payment_date': time.strftime('%Y-%m-%d'),
            'amount': 500,
        })
        # Mark as Paid
        self.wf_service.trg_validate(uid, 'pos.order', po_id, 'paid', cr)

        # Sub Test 2 : Try Invoice : Must Succeed
        res = self.po_obj.action_invoice(cr, uid, [po_id])
        inv_id = res.get('res_id', 0)
        self.assertEquals(
            inv_id != 0, True, "A Pos Order must to be invoiceable!")

        # Open the invoice
        self.wf_service.trg_validate(
            uid, 'account.invoice', inv_id, 'invoice_open', cr)

        # Close Session
        self.wf_service.trg_validate(uid, 'pos.session', ps_id, 'close', cr)

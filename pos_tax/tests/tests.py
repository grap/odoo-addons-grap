# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Tax Module for Odoo
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


class TestPosTax(TransactionCase):

    def setUp(self):
        super(TestPosTax, self).setUp()
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
        self.product_1 = self.imd_obj.get_object_reference(
            cr, uid, 'product', 'product_product_48')[1]
        self.pos_config_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        self.cash_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'cash_journal')[1]
        self.sale_journal_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'sales_journal')[1]

    # Test Section
    def test_01_close_session_with_taxes_changed(self):
        """[Functional Test] Test if sale in POS product with VAT change
         generate correct account entries"""
        cr, uid = self.cr, self.uid

        # Create Tax
        at_id = self.at_obj.create(cr, uid, {
            'name': 'Demo Tax 10% VAT Excl',
            'amount': 0.1,
            'price_include': False,
        })

        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])

        # Create Order #1
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
        })
        # Create Order line #1
        self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_1,
            'name': 'Product 1 - Account 1',
            'price_unit': 10,
        })
        # Make Payement
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 10,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})

        # Add Taxes to Product
        self.pp_obj.write(cr, uid, self.product_1, {
            'taxes_id': [[6, False, [at_id]]]})

        # Create Order #2
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
        })
        # Create Order line #2
        pol_id = self.pol_obj.create(cr, uid, {
            'order_id': po_id,
            'product_id': self.product_1,
            'name': 'Product 1',
            'price_unit': 2000,
        })
        self.pol_obj.onchange_qty(
            cr, uid, [pol_id], self.product_1, 0, 1, 2000)
        # Make Payement
        pmp_id = self.pmp_obj.create(cr, uid, {
            'journal_id': self.cash_journal_id,
            'amount': 2200,
        })
        self.pmp_obj.check(cr, uid, [pmp_id], {'active_id': po_id})
        wf_service = netsvc.LocalService('workflow')

        # FIXME : Extra
        # Compute and set final Total Transaction
        # Note: Not so clean, but due to other module
        # 'pos_multiple_cash_control'
        if len(self.imm_obj.search(cr, uid, [
                ('name', '=', 'pos_multiple_cash_control'),
                ('state', '=', 'installed')])) == 1:
            abs_id = self.abs_obj.search(cr, uid, [
                ('journal_id', '=', self.cash_journal_id)], order='id DESC')[0]
            self.abs_obj.write(cr, uid, [abs_id], {
                'details_ids': [[0, False, {
                    'pieces': 2210,
                    'number_closing': 1}]]})

            wf_service.trg_validate(
                uid, 'pos.session', ps_id, 'cashbox_control', cr)
        # End of Patch

        # Close Session
        wf_service.trg_validate(
            uid, 'pos.session', ps_id, 'close', cr)

        ps = self.ps_obj.browse(cr, uid, ps_id)
        # Check Sale Move
        sale_move_id = self.am_obj.search(cr, uid, [
            ('ref', '=', ps.name),
            ('journal_id', '=', self.sale_journal_id)])

        sale_move = self.am_obj.browse(cr, uid, sale_move_id[0])

        credit = debit = 0
        for line in sale_move.line_id:
            credit += line.credit
            debit += line.debit

        self.assertEquals(
            credit, debit,
            """Validate POS session must created balanced Sale Move,"""
            """Even if Taxes of Products have changed.""")

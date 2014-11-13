# -*- encoding: utf-8 -*-
##############################################################################
#
#    Module - Parent Dependencies module for Odoo
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

from openerp.tests.common import TransactionCase
from openerp.osv.orm import except_orm


class TestPosMultipleCashControl(TransactionCase):
    """Tests for 'Point Of Sale - Multiple Cash Control' Module"""

    def setUp(self):
        super(TestPosMultipleCashControl, self).setUp()
        cr, uid = self.cr, self.uid
        self.imd_obj = self.registry('ir.model.data')
        self.pp_obj = self.registry('product.product')
        self.ru_obj = self.registry('res.users')
        self.at_obj = self.registry('account.tax')
        self.ps_obj = self.registry('pos.session')
        self.account_manager_group_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'group_account_manager')[1]
        self.account_group_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'group_account_user')[1]
        self.account_income_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_sale')[1]
        self.account_expense_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_expense')[1]
        self.pc_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
        self.tax_30 = self.imd_obj.get_object_reference(
            cr, uid, 'pos_multiple_cash_control', 'account_tax_30')[1]
        self.tax_50 = self.imd_obj.get_object_reference(
            cr, uid, 'pos_multiple_cash_control', 'account_tax_50')[1]

    def test_01_check_access_right(self):
        """Test Multiple access right Control"""
        pass
        cr, uid = self.cr, self.uid
        self.ru_obj.write(cr, uid, [uid], {
            'groups_id': [(6, 0, [self.account_group_id])],
        })

        vals = {
            'name': 'Test Product',
            'sale_ok': False,
            'purchase_ok': False,
            'property_account_expense': self.account_expense_id,
            'property_account_income': self.account_income_id,
            'expense_pdt': True}
        # Try to create Expend Product without right
        error = False
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "Basic user has no right to create an expense POS Product.")

        # Try to create Income Product without right
        vals.pop('expense_pdt')
        vals['income_pdt'] = True
        error = False
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "Basic user has no right to create an income POS Product.")

        # Try to create Income Product with right
        self.ru_obj.write(cr, uid, [uid], {
            'groups_id': [(6, 0, [self.account_manager_group_id])],
        })
        error = False
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, False,
            "Account Manager user has right to create an income POS Product.")

    def test_02_check_constraint(self):
        """Test Multiple Contraint"""
        pass
        # Try to create Income Product salable
        cr, uid = self.cr, self.uid
        self.ru_obj.write(cr, uid, [uid], {
            'groups_id': [(6, 0, [self.account_manager_group_id])],
        })

        vals = {
            'name': 'Test Product',
            'sale_ok': True,
            'purchase_ok': False,
            'property_account_expense': self.account_expense_id,
            'property_account_income': self.account_income_id,
            'expense_pdt': True}
        error = False
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "You can not create a POS Product salable.")

        # Try to create product with many taxes
        error = False
        vals['sale_ok'] = False
        vals['supplier_taxes_id'] = [[6, False, [self.tax_50, self.tax_30]]]
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "Create a POS Product Expense with many taxes must Fail.")

        # Try to create product with one taxe
        error = False
        vals['supplier_taxes_id'] = [[6, False, [self.tax_50]]]
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, False,
            "Create a POS Product with on tax must succeed.")

        # Try to create POS product Expense without account_expense
        error = False
        vals.pop('property_account_expense')
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "Create a POS Product Expense without account_expense must fail.")

        # Try to create POS product Expense without account_income
        error = False
        vals.pop('property_account_income')
        vals.pop('expense_pdt')
        vals['property_account_expense'] = self.account_expense_id
        vals['income_pdt'] = True
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, True,
            "Create a POS Product Income without account_income must fail.")

        # Final test must succeed
        error = False
        vals.pop('property_account_expense')
        vals['property_account_income'] = self.account_income_id
        try:
            self.pp_obj.create(cr, uid, vals)
        except except_orm:
            error = True
        self.assertEqual(
            error, False,
            "Create a POS Product must succeed.")

    def test_02_check_open_session(self):
        """Test Open Session"""
        cr, uid = self.cr, self.uid
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pc_id,
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])

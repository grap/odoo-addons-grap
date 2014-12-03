# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category - Recursive property for Odoo
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


class TestProductCategoryRecursiveProperty(TransactionCase):

    def setUp(self):
        super(TestProductCategoryRecursiveProperty, self).setUp()
        cr, uid = self.cr, self.uid
        self.imd_obj = self.registry('ir.model.data')
        self.pc_obj = self.registry('product.category')
        self.ip_obj = self.registry('ir.property')
        self.mother_pc_id = self.imd_obj.get_object_reference(
            cr, uid, 'product_category_recursive_property',
            'mother_category')[1]
        self.child_pc_id = self.imd_obj.get_object_reference(
            cr, uid, 'product_category_recursive_property',
            'child_category')[1]
        self.income_ip_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'property_account_income_categ')[1]
        self.expense_ip_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'property_account_expense_categ')[1]
        self.expense_aa_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_sale')[1]
        self.income_aa_id = self.imd_obj.get_object_reference(
            cr, uid, 'account', 'a_expense')[1]

    # Test Section
    def test_01_all_default(self):
        """[Functional Test] Tests changing expense / income account
        on product categories"""
        cr, uid = self.cr, self.uid

        # Delete default property value
        self.ip_obj.unlink(cr, uid, [self.income_ip_id, self.expense_ip_id])
        pc_ids = self.pc_obj.search(cr, uid, [])
        for pc in self.pc_obj.browse(cr, uid, pc_ids):
            self.assertEquals(
                pc.property_account_expense_categ.id, False,
                "Regression - Remove default value must remove expense"
                " property !")
            self.assertEquals(
                pc.property_account_income_categ.id, False,
                "Regression - Remove default value must remove income"
                " property !")

        # Set expense categ to mother pc
        self.pc_obj.write(cr, uid, [self.mother_pc_id], {
            'property_account_expense_categ': self.expense_aa_id})
        child_pc = self.pc_obj.browse(cr, uid, self.child_pc_id)
        self.assertEquals(
            child_pc.property_account_expense_categ.id, self.expense_aa_id,
            "Set an expense account to a mother category must set an"
            " expense account to their childs !")

        # Set income categ to mother pc
        self.pc_obj.write(cr, uid, [self.mother_pc_id], {
            'property_account_income_categ': self.income_aa_id})
        child_pc = self.pc_obj.browse(cr, uid, self.child_pc_id)
        self.assertEquals(
            child_pc.property_account_income_categ.id, self.income_aa_id,
            "Set an income account to a mother category must set an"
            " income account to their childs !")

        # Check if other categories are not affected
        pc_ids = self.pc_obj.search(cr, uid, [
            ('id', 'not in', [self.mother_pc_id, self.child_pc_id])])
        for pc in self.pc_obj.browse(cr, uid, pc_ids):
            self.assertEquals(
                pc.property_account_expense_categ.id, False,
                "Set an expense categ to a category must not affect non child"
                " categories !")
            self.assertEquals(
                pc.property_account_income_categ.id, False,
                "Set an income categ to a category must not affect non child"
                " categories !")

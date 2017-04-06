# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductCategoryRecursiveProperty(TransactionCase):

    def setUp(self):
        super(TestProductCategoryRecursiveProperty, self).setUp()
        self.category_obj = self.env['product.category']
        self.property_obj = self.env['ir.property']
        self.mother_category = self.env.ref(
            'product_category_recursive_property.mother_category')
        self.child_category = self.env.ref(
            'product_category_recursive_property.child_category')
        self.income_account_property = self.env.ref(
            'account.property_account_income_categ')
        self.expense_account_property = self.env.ref(
            'account.property_account_expense_categ')
        self.expense_account = self.env.ref('account.a_sale')
        self.income_account = self.env.ref('account.a_expense')

    # Test Section
    def test_01_all_default(self):
        """[Functional Test] Tests changing expense / income account
        on product categories"""

        # Delete default property value
        self.income_account_property.unlink()
        self.expense_account_property.unlink()
        for category in self.category_obj.search([]):
            self.assertEquals(
                category.property_account_expense_categ.id, False,
                "Regression - Remove default value must remove expense"
                " property !")
            self.assertEquals(
                category.property_account_income_categ.id, False,
                "Regression - Remove default value must remove income"
                " property !")

        # Set expense categ to mother category
        self.mother_category.write({
            'property_account_expense_categ': self.expense_account.id})
        self.assertEquals(
            self.child_category.property_account_expense_categ.id,
            self.expense_account.id,
            "Set an expense account to a mother category must set an"
            " expense account to their childs !")

        # Set income categ to mother category
        self.mother_category.write({
            'property_account_income_categ': self.income_account.id})
        self.assertEquals(
            self.child_category.property_account_income_categ.id,
            self.income_account.id,
            "Set an income account to a mother category must set an"
            " income account to their childs !")

        # Check if other categories are not affected
        categories = self.category_obj.search([
            ('id', 'not in', [
                self.mother_category.id, self.child_category.id])])
        for category in categories:
            self.assertEquals(
                category.property_account_expense_categ.id, False,
                "Set an expense categ to a category must not affect non child"
                " categories !")
            self.assertEquals(
                category.property_account_income_categ.id, False,
                "Set an income categ to a category must not affect non child"
                " categories !")

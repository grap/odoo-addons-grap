# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Inventory - Sum Duplicates for Odoo
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

from openerp.tests.common import TransactionCase


#class TestAccountGroupMoveLines(TransactionCase):

#    def setUp(self):
#        super(TestAccountGroupMoveLines, self).setUp()
#        cr, uid = self.cr, self.uid
#        self.imd_obj = self.registry('ir.model.data')
#        self.si_obj = self.registry('stock.inventory')
#        self.stock_inventory_id = self.imd_obj.get_object_reference(
#            cr, uid, 'stock_inventory_sum_duplicates',
#            'stock_inventory_sum_duplicates')[1]
#        self.stock_location_1_id = self.imd_obj.get_object_reference(
#            cr, uid, 'stock',
#            'stock_location_components')[1]
#        self.stock_location_2_id = self.imd_obj.get_object_reference(
#            cr, uid, 'stock',
#            'stock_location_14')[1]
#        self.product_1_id = self.imd_obj.get_object_reference(
#            cr, uid, 'product',
#            'product_product_48')[1]
#        self.product_2_id = self.imd_obj.get_object_reference(
#            cr, uid, 'product',
#            'product_product_24')[1]

#    # Test Section
#    def test_01_confirm_stock_inventory(self):
#        """[Functional Test] Confirm Stock Inventory with many references to
#        the same products"""
#        cr, uid = self.cr, self.uid
#        self.si_obj.action_confirm(cr, uid, [self.stock_inventory_id])

#        si = self.si_obj.browse(cr, uid, self.stock_inventory_id)

#        self.assertEquals(
#            len(si.inventory_line_id), 3,
#            """Merge Failed : Incorrect Number of lines.""")

#        # Test if merge is realized or not
#        lineNumber = 0
#        for line in si.inventory_line_id:
#            if (
#                    line.location_id.id == self.stock_location_1_id and
#                    line.product_id.id == self.product_1_id):
#                lineNumber += 1
#                self.assertEquals(
#                    line.product_qty, 31,
#                    """Merge Failed: Incorrect Quantity after merge.""")
#            elif (
#                    line.location_id.id == self.stock_location_1_id and
#                    line.product_id.id == self.product_2_id):
#                self.assertEquals(
#                    line.product_qty, 32,
#                    """Quantity changed, behaviour not expected.""")
#            elif (
#                    line.location_id.id == self.stock_location_2_id and
#                    line.product_id.id == self.product_1_id):
#                self.assertEquals(
#                    line.product_qty, 43,
#                    """Quantity changed, behaviour not expected.""")
#            else:
#                self.assertEquals(
#                    True, False,
#                    """Unexpected Line""")

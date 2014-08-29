# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multi Company Context module for OpenERP
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
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

from openerp.osv import osv, orm
from openerp.tests.common import TransactionCase


class TestPosMulticompany(TransactionCase):
    """Tests for POS Multicompany Module"""

    def setUp(self):
        super(TestPosMulticompany, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.pcat_obj = self.registry('pos.category')
        self.rc_obj = self.registry('res.company')

    # Test Section
    def test_01_create_several_pos_category(self):
        """[regression test] Create several pos category"""

        cr, uid = self.cr, self.uid
        # Getting object
        pcat_fruits_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'fruits')[1]
        self.pcat_obj.create(cr, uid, {
            'name': 'TEST 1',
            'parent_id': pcat_fruits_id,
        })
        self.pcat_obj.create(cr, uid, {
            'name': 'TEST 2',
            'parent_id': pcat_fruits_id,
        })

    def test_02_create_multiple_default_pos_category(self):
        """[Functional Test] Try to create several default category"""
        cr, uid = self.cr, self.uid
        error = False
        rc_id = self.imd_obj.get_object_reference(
            cr, uid, 'base', 'main_company')[1]
        try:
            self.pcat_obj.create(cr, uid, {
                'name': 'TEST 1',
                'is_default': True,
                'company_id': rc_id,
            })
        except orm.except_orm:
            error = True
        self.assertEquals(
            error, True, "Creating multiple default category must fail!")

    def test_03_delete_default_pos_category(self):
        """[Functional Test] Try to delete the default pos_category"""
        cr, uid = self.cr, self.uid
        error = False
        pcat_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'categ_others')[1]
        try:
            self.pcat_obj.unlink(cr, uid, [pcat_id])
        except osv.except_osv:
            error = True
        self.assertEquals(
            error, True, "Deleting default pos category must fail!")

    def test_04_create_res_company(self):
        """[Functional Test] Create a res company must create a"""
        """ default pos category"""
        cr, uid = self.cr, self.uid
        rc_id = self.rc_obj.create(cr, uid, {
            'name': 'Company 1',
        })
        pcat_id = self.pcat_obj._get_pos_categ_id_by_company(cr, uid, rc_id)
        self.assertNotEquals(
            pcat_id, False, "Creating a company must create a pos category!")

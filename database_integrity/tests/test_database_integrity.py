# -*- encoding: utf-8 -*-
##############################################################################
#
#    Database Integrity module for OpenERP
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
from psycopg2 import IntegrityError
from openerp.exceptions import AccessError

class TestDatabaseIntegrity(TransactionCase):
    """Tests for 'DataBase Integrity' Module"""

    def setUp(self):
        super(TestDatabaseIntegrity, self).setUp()
        self.disw_obj = self.registry('database.integrity.sequence.wizard')
        self.imd_obj = self.registry('ir.model.data')
        self.rp_obj = self.registry('res.partner')

    # Test Section
    def test_01_sequence_integrity_valid(self):
        """Test if the wizard has correct behaviour by default."""
        cr, uid = self.cr, self.uid
        disw_id = self.disw_obj.create(cr, uid, {})
        disw = self.disw_obj.browse(cr, uid, disw_id)
        qty = 0
        for diswl in disw.line_ids:
            if diswl.state == 'invalid':
                qty += 1
        self.assertEqual(
            qty, 0,
            "There is no invalid sequence on a default test database.")

    def test_02_sequence_integrity_invalid_create(self):
        """Test the sequences check and the fix workflow."""
        cr, uid = self.cr, self.uid
        # Put an invalid sequence on res_partner table
        cr.execute("ALTER SEQUENCE res_partner_id_seq RESTART WITH 1;")

        # Test if we can create a res.partner. Must Fail
        error = False
        try:
            self.rp_obj.create(cr, uid, {'name': 'Test Sequence'})
        except IntegrityError:
            error = True
        self.assertEqual(
            error, True,
            "Partner creation must fail with invalid sequence.")

    def test_03_sequence_integrity_invalid_analyze(self):
        """Test the sequences check and the wizard analyse."""
        cr, uid = self.cr, self.uid

        # Test if the wizard analyze correctly the invalid sequence
        disw_id = self.disw_obj.create(cr, uid, {})
        disw = self.disw_obj.browse(cr, uid, disw_id)
        qty = 0
        for diswl in disw.line_ids:
            if diswl.state == 'invalid':
                qty += 1
        self.assertEqual(
            qty, 1,
            "Incorrect invalid sequences quantity.")

        # Run the wizard to fix sequence
        self.disw_obj.fix_invalid_sequence(cr, uid, [disw_id])

    def test_04_sequence_integrity_invalid_fix(self):
        """Test the wizard fix."""
        cr, uid = self.cr, self.uid

        # Test if the sequence is now correct
        cr.execute("SELECT last_value FROM res_partner_id_seq;")
        last_value = cr.fetchone()[0]

        cr.execute("SELECT max(id) FROM res_partner;")
        max_id = cr.fetchone()[0]
        self.assertEqual(
            last_value, max_id,
            "Sequence Value and Max(id) must be identical after wizard.")

    # Test Section
    def test_05_access(self):
        """Test if the wizard can be launched by basic user.."""
        cr, uid = self.cr, self.uid
        uid = self.imd_obj.get_object_reference(cr, uid, 'base', 'user_demo')[1]
        disw_id = self.disw_obj.create(cr, uid, {})
        error = False
        try:
            self.disw_obj.fix_invalid_sequence(cr, uid, disw_id)
        except AccessError:
            error = True
        self.assertEqual(
            error, True,
            "Sequence manipulation musn't be available for basic users.")

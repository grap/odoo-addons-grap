# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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


class TestAccountExportEBP(TransactionCase):
    """Tests for Account Export EBP Module"""

    def setUp(self):
        super(TestAccountExportEBP, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.ai_obj = self.registry('account.invoice')
        self.am_obj = self.registry('account.move')
        self.aml_obj = self.registry('account.move.line')
        self.webp_obj = self.registry('account.export.ebp')
        self.afy_obj = self.registry('account.fiscalyear')

    ### Test Section
    def test_01_export_ref_null(self):
        """Test the export if move ref is null"""
        cr, uid = self.cr, self.uid
        # Get a demo account move
        ai_id = self.imd_obj.get_object_reference(cr, uid, 'account', 'test_invoice_1')[1]
        ai = self.ai_obj.browse(cr, uid, ai_id)
        am = ai.move_id
        afy_id = self.imd_obj.get_object_reference(cr, uid, 'account', 'data_fiscalyear')[1]

        # Setting 'ref' field to Null
        aml_ids = [aml.id for aml in am.line_id]
        self.aml_obj.write(cr, uid, aml_ids, {'ref': False})

        # Call wizard to export lines
        vals = {
            'fiscalyear_id': afy_id,
            'download_file': True,
        }
        ctx = {
            'active_model': 'account.move',
            'active_ids': [ai.move_id.id],
            'ignore_draft': True,
        }
        webp_id = self.webp_obj.create(cr, uid, vals)
        self.webp_obj.export(cr, uid, [webp_id], context=ctx)

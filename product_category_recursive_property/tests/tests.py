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
        self.imd_obj = self.registry('ir.model.data')
        self.pp_obj = self.registry('product.product')
        self.ppl_obj = self.registry('product.pricelist')
        self.po_obj = self.registry('pos.order')
        self.pol_obj = self.registry('pos.order.line')
        self.pc_obj = self.registry('pos.config')
        self.ps_obj = self.registry('pos.session')

    # Test Section
    def test_01_default_price_list(self):
        """[Functional Test] Change """
#        cr, uid = self.cr, self.uid
#        # Getting object
#        pc_id = self.imd_obj.get_object_reference(
#            cr, uid, 'point_of_sale', 'pos_config_main')[1]
#        rp_c2c_id = self.imd_obj.get_object_reference(
#            cr, uid, 'base', 'res_partner_12')[1]
#        ppl_c2c_id = self.imd_obj.get_object_reference(
#            cr, uid, 'product', 'list0')[1]
#        pp_usb_id = self.imd_obj.get_object_reference(
#            cr, uid, 'product', 'product_product_48')[1]

#        # Opening Session
#        self.ps_obj.create(cr, uid, {
#            'config_id': pc_id,
#        })

#        # create Pos Order
#        po_id = self.po_obj.create(cr, uid, {
#            'partner_id': rp_c2c_id,
#            'pricelist_id': ppl_c2c_id,
#            'lines': [[0, False, {
#                'product_id': pp_usb_id,
#                'qty': 1,
#            }]],
#        })
#        pp_usb = self.pp_obj.browse(cr, uid, pp_usb_id)
#        po = self.po_obj.browse(cr, uid, po_id)

#        res = self.pol_obj.onchange_product_id(
#            cr, uid, po.lines[0].id, po.pricelist_id.id,
#            po.lines[0].product_id.id, po.lines[0].qty)

#        self.assertEquals(
#            res['value']['price_subtotal'], pp_usb.list_price,
#            "Incorrect price for default pricelist!")

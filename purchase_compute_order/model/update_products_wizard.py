# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv.orm import TransientModel
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class update_products_wizard(TransientModel):
    _name = 'update.products.wizard'
    _description = 'Update product_supplierinfo from compute_purchase_order'

#    ### Overloading section
    def default_get(self, cr, uid, fields, context):
        line_ids = []
        res = super(update_products_wizard, self).default_get(cr, uid, fields, context=context)
        active_id = context.get('active_id', False)
        if active_id:
            psi_obj = self.pool.get('product.supplierinfo')
            cpo = self.pool.get('computed.purchase.order').browse(cr, uid, active_id, context=context)
            updated_lines = [x.id for x in cpo.line_ids if x.state == 'updated']
            cpol = self.pool.get('computed.purchase.order.line').browse(cr, uid, updated_lines, context=context)
            values = {}
            for line in cpol:
                psi_id = psi_obj.search(cr, uid, [
                    ('name', '=', line.computed_purchase_order_id.partner_id.id), 
                    ('product_id', '=', line.product_id.product_tmpl_id.id)
                    ], context=context)[0]
                
                line_ids.append((0, 0, {
                    'product_id': line.product_id.id,
                    'supplierinfo_id': psi_id,
                    'product_code': line.product_code,
                    'product_name': line.product_name,
                    'product_uom': line.uom_po_id.id,
                    'package_qty': line.package_quantity,
                    'price': line.product_price,
                    'computed_purchase_order_line_id': line.id,
                    }))
            res.update({'line_ids': line_ids})
        return res

    ### Columns
    _columns = {
        'line_ids': fields.one2many('update.products.line.wizard', 'wizard_id', 'Updated Products list'),
    }

    ### Action section
    def apply_product_change(self, cr, uid, ids, context=None):
        psi_obj = self.pool.get('product.supplierinfo')
        ppi_obj = self.pool.get('pricelist.partnerinfo')
        cpol_obj = self.pool.get('computed.purchase.order.line')
        cpol_ids = []
        for upw in self.browse(cr, uid, ids, context=context):
            for line in upw.line_ids:
                ppi_ids = []
                for price in line.supplierinfo_id.pricelist_ids:
                    ppi_ids += [price.id]
                ppi_obj.unlink(cr, uid, ppi_ids, context=context)
                values = {
                    'product_name': line.product_name,
                    'product_code': line.product_code,
                    'product_uom': line.product_uom.id,
                    'package_qty': line.package_qty,
                    'product_id' : line.product_id.product_tmpl_id.id,
                    'pricelist_ids': [(0,0, {
                                'suppinfo_id': line.supplierinfo_id.id,
                                'min_quantity': 0,
                                'price': line.price,
                                })],
                }
                psi_obj.write(cr, uid, [line.supplierinfo_id.id], values , context=context)
                cpol_ids += [line.computed_purchase_order_line_id.id]
        cpol_obj.write(cr, uid, cpol_ids, {'state': 'up_to_date'}, context=context)
        return True


class update_products_line_wizard(TransientModel):
    _name = "update.products.line.wizard"
    _description = "Information about products to update"

    ### Columns section
    _columns = {
        'wizard_id': fields.many2one('update.products.wizard', 'Wizard Reference', select=True),
        'product_id' : fields.many2one('product.product', 'Product', required=True, ondelete='cascade', select=True),
        'supplierinfo_id': fields.many2one('product.supplierinfo', 'Partner Information', required=True, ondelete='cascade'),
        'product_code': fields.char('Supplier Product Code', size=64, help="This supplier's product code will be used when printing a request for quotation. Keep empty to use the internal one."),
        'product_name': fields.char('Supplier Product Name', size=128, help="This supplier's product name will be used when printing a request for quotation. Keep empty to use the internal one."),
        'product_uom': fields.many2one('product.uom', "Supplier Unit of Measure", required=True, help="This comes from the product form."),
        'package_qty': fields.float('Package Quantity', required=True, help="The minimal quantity to purchase to this supplier, expressed in the supplier Product Unit of Measure if not empty, in the default unit of measure of the product otherwise."),
        'price': fields.float('Unit Price', required=True, digits_compute=dp.get_precision('Product Price'), help="This price will be considered as a price for the supplier Unit of Measure if any or the default Unit of Measure of the product otherwise"),
        'computed_purchase_order_line_id': fields.many2one('computed.purchase.order.line', 'Ligne de Calcul', required=True, ondelete='cascade', select=True),
    }

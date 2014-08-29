# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class computed_purchase_order_line(Model):
    _description="Computed Purchase Order Line"
    _name = 'computed.purchase.order.line'
    _order = 'sequence'

    _STATE = [
        ('new', 'New'),
        ('up_to_date', 'Up to date'),
        ('updated', 'Updated'),
    ]
    
    ### Functions columns section
    def _get_qty_available(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] =  cpol.product_id.qty_available
        return res

    def _get_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = {
                'incoming_qty': cpol.product_id.incoming_qty,
                'outgoing_qty': cpol.product_id.outgoing_qty,
                }
        return res

    def _get_draft_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = {
                'draft_incoming_qty': cpol.product_id.draft_incoming_qty,
                'draft_outgoing_qty': cpol.product_id.draft_outgoing_qty,
                }
        return res

    def _get_computed_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = self._get_qty_available(cr, uid, ids, field_name, arg, context=context)
        
        use_pending_qties = False
        use_draft_qties = False
        for cpol in self.browse(cr, uid, ids, context=context):
            if cpol.computed_purchase_order_id.compute_pending_quantity:
                use_pending_qties = True
            if cpol.computed_purchase_order_id.compute_draft_quantity:
                use_draft_qties = True
            if use_pending_qties and use_draft_qties:
                break
        
        fields=[]
        if use_pending_qties:
            fields += ['incoming_qty', 'outgoing_qty']
        if use_draft_qties:
            fields += ['draft_incoming_qty', 'draft_outgoing_qty']
        
        if fields:
            qties = self.read(cr, uid, ids, fields, context=context)
            for x in qties:
                res[x['id']] += sum([x[f] for f in fields])
        return res

    def _get_product_information(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        psi_obj = self.pool.get('product.supplierinfo')
        pp_obj = self.pool.get('product.product')
        for cpol in self.browse(cr, uid, ids, context=context):
            if not cpol.product_id: 
                res[cpol.id] = {
                    'product_code_inv': None, 
                    'product_name_inv': None, 
                    'product_price_inv': 0.0,
                    'package_quantity_inv': 0.0,
                    }
            elif cpol.state in ('updated', 'new'):
                res[cpol.id] = {
                    'product_code_inv': cpol.product_code, 
                    'product_name_inv': cpol.product_name,
                    'product_price_inv': cpol.product_price,
                    'package_quantity_inv': cpol.package_quantity,
                    }
            else:
                psi_ids = psi_obj.search(cr, uid, [('name', '=', cpol.computed_purchase_order_id.partner_id.id), 
                    ('product_id', '=', cpol.product_id.product_tmpl_id.id)], context=context)
                if psi_ids: 
                    psi = psi_obj.browse(cr, uid, psi_ids[0], context=context)
                    res[cpol.id] = {
                        'product_code_inv': psi.product_code, 
                        'product_name_inv': psi.product_name,
                        'product_price_inv': psi.pricelist_ids 
                            and psi.pricelist_ids[0].price 
                            or psi.product_id.standard_price, 
                        'package_quantity_inv': psi.package_qty
                        }
        return res

    def _set_product_code(self, cr, uid, id, field_name, field_value, args, context=None):
        vals = {'product_code': field_value}
        if self.browse(cr, uid, id, context=context).state == 'up_to_date':
             vals.update({'state': 'updated'})
        return self.write(cr, uid, id, vals, context=context)

    def _set_product_name(self, cr, uid, id, field_name, field_value, args, context=None):
        vals = {'product_name': field_value}
        if self.browse(cr, uid, id, context=context).state == 'up_to_date':
             vals.update({'state': 'updated'})
        return self.write(cr, uid, id, vals, context=context)

    def _set_product_price(self, cr, uid, id, field_name, field_value, args, context=None):
        vals = {'product_price': field_value}
        if self.browse(cr, uid, id, context=context).state == 'up_to_date':
             vals.update({'state': 'updated'})
        return self.write(cr, uid, id, vals, context=context)

    def _set_package_quantity(self, cr, uid, id, field_name, field_value, args, context=None):
        vals = {'package_quantity': field_value}
        if self.browse(cr, uid, id, context=context).state == 'up_to_date':
             vals.update({'state': 'updated'})
        return self.write(cr, uid, id, vals, context=context)

    def _compute_stock_duration(self, cr, uid, ids, field_name, field_value, args, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            if not cpol.product_id: 
                res[cpol.id] = False
            else:
                if cpol.average_consumption == 0:
                    res[cpol.id] = False
                else:
                    res[cpol.id] = (cpol.computed_qty + cpol.manual_input_output_qty) / cpol.average_consumption
        return res

    def _store_stock_duration (self, cr, uid, ids, context=None):
        return self._compute_stock_duration(cr, uid, ids, 'stock_duration', 0, None, context=None)

    def _get_draft_outgoing_qty (self, cr, uid, ids, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = cpol.product_id.draft_outgoing_qty
        return res

    def _get_draft_incoming_qty (self, cr, uid, ids, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = cpol.product_id.draft_incoming_qty
        return res

    def _get_outgoing_qty (self, cr, uid, ids, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = cpol.product_id.outgoing_qty
        return res

    def _get_incoming_qty (self, cr, uid, ids, context=None):
        res = {}
        for cpol in self.browse(cr, uid, ids, context=context):
            res[cpol.id] = cpol.product_id.incoming_qty
        return res

    ### Columns section
    _columns = {
        'computed_purchase_order_id': fields.many2one('computed.purchase.order', 'Order Reference', required=True, ondelete='cascade'),
        'state': fields.selection(_STATE,'State', required=True, readonly=True,
            help="Shows if the product's information has been updated"),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of purchase order lines."),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'uom_id': fields.related('product_id', 'uom_id', string="UoM", type='many2one', relation='product.uom', readonly='True'),
        'product_code': fields.char('Supplier Product Code',),
        'product_code_inv': fields.function(_get_product_information, fnct_inv=_set_product_code, 
            type='char', string='Supplier Product Code',
            multi='product_code_name_price',
            help="This supplier's product code will be used when printing a request for quotation. Keep empty to use the internal one."),
        'product_name': fields.char('Supplier Product Name',),
        'product_name_inv': fields.function(_get_product_information, fnct_inv=_set_product_name, 
            type='char', string='Supplier Product Name', 
            multi='product_code_name_price',
            help="This supplier's product name will be used when printing a request for quotation. Keep empty to use the internal one."),
        'product_price': fields.float('Supplier Product Price', digits_compute=dp.get_precision('Product Price')),
        'product_price_inv': fields.function(_get_product_information, fnct_inv=_set_product_price, 
            type='float', string='Supplier Product Price', 
            multi='product_code_name_price',),
        'package_quantity': fields.float('Package quantity'),
        'package_quantity_inv': fields.function(_get_product_information, fnct_inv=_set_package_quantity, 
            type='float', string='Package quantity', 
            multi='product_code_name_price',),
        'weight_net': fields.related('product_id', 'weight_net', string="Net Weight", type='float', readonly='True'),
        'uom_po_id': fields.many2one('product.uom', 'UoM', required=True),

        'average_consumption': fields.float("Average Consumption", digits=(12,3)),
        'stock_duration': fields.function(_compute_stock_duration, string="Stock Duration (Days)", type='float', readonly='True', help="Number of days the stock should last.", 
            ),
        'purchase_qty': fields.float('Quantity to purchase', required=True,
            help="The quantity you should purchase."),
        'manual_input_output_qty': fields.float(string='Manual variation', 
            help="""Write here some extra quantity depending of some input or output of products not entered in the software\n
                - negative quantity : extra output ; \n
                - positive quantity : extra input."""),
        'qty_available': fields.function(_get_qty_available, type='float', string='Quantity On Hand', 
            help="The available quantity on hand for this product"),
        'incoming_qty': fields.function(_get_qty, type='float', string='Incoming Quantity', 
            help="Virtual incoming entries", multi='get_qty',
            store=True
            ),
        'outgoing_qty': fields.function(_get_qty, type='float', string='Outgoing Quantity', 
            help="Virtual outgoing entries", multi='get_qty',
            store=True
            ),
        'draft_incoming_qty': fields.function(_get_draft_qty, type='float', string='Draft Incoming Quantity', 
            help="Draft purchases", multi='get_draft_qty',
            store=True
            ),
        'draft_outgoing_qty': fields.function(_get_draft_qty, type='float', string='Draft Outgoing Quantity', 
            help="Draft sales", multi='get_draft_qty',
            store=True
            ),
        'computed_qty': fields.function(_get_computed_qty, type='float', string='Stock', 
            help="The sum of all quantities selected.", 
            digits_compute=dp.get_precision('Product UoM'),),
    }

    ### SQL Constraints section
    _sql_constraints = [
        ('product_id_uniq','unique(computed_purchase_order_id,product_id)', 'Product must be unique by computed purchase order!'),
    ]


    ### Defaults section
    _defaults = {
        'state': 'new',
        'purchase_qty': 0, 
        'manual_input_output_qty': 0,
    }

    ### View Section
    def onchange_product_info(self, cr, uid, ids, context=None):
        return {'value': {'state': 'updated'}}

    def onchange_product_id(self, cr, uid, ids, parent_id, product_id, partner_id, context=None):
        if not product_id: 
            vals = self._defaults
        else: 
            psi_obj = self.pool.get('product.supplierinfo')
            pp = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            vals = self._defaults
            computed_qty = pp.qty_available

            if parent_id:
                cpo = self.pool.get('computed.purchase.order').browse(cr, uid, parent_id, context=context)
                #Check if the product is already in the list.
                products = [x.product_id.id for x in cpo.line_ids]
                if product_id in products:
                    raise osv.except_osv(_('Invalid Action!'), _('This product is already in the list!'))

                if cpo.compute_pending_quantity: 
                    computed_qty += pp.incoming_qty + pp.outgoing_qty
                if cpo.compute_draft_quantity: 
                    computed_qty += pp.draft_incoming_qty + pp.draft_outgoing_qty

            vals.update({
                'qty_available': pp.qty_available,
                'incoming_qty': pp.incoming_qty,
                'outgoing_qty': pp.outgoing_qty,
                'draft_incoming_qty': pp.draft_incoming_qty,
                'draft_outgoing_qty': pp.draft_outgoing_qty,
                'computed_qty': computed_qty,
                'weight_net': pp.weight_net,
                'uom_po_id': pp.uom_id.id, 
                'product_price_inv': 0,
                'package_quantity_inv': 0,
                'average_consumption': pp.average_consumption,
            })

            # If product is in the supplierinfo, retrieve values and set state up_to_date
            psi_id = psi_obj.search(cr, uid, [('name', '=', partner_id), ('product_id', '=', pp.product_tmpl_id.id)], context=context)
            if psi_id:
                psi = psi_obj.browse(cr, uid, psi_id, context=context)[0]
                vals.update({
                    'product_code_inv': psi.product_code,
                    'product_name_inv': psi.product_name,
                    'product_price_inv': psi.pricelist_ids and psi.pricelist_ids[0].price or 0,
                    'package_quantity_inv': psi.package_qty, 
                    'uom_po_id': psi.product_uom.id, 
                    'state': 'up_to_date', 
                })
        return {'value': vals}

    def unlink_psi(self, cr, uid, ids, context=None):
        psi_obj = self.pool.get("product.supplierinfo")
        cpol_obj = self.pool.get("computed.purchase.order.line")
        psi2unlink = []
        for cpol in self.browse(cr, uid, ids, context=context):
            cpo = cpol.computed_purchase_order_id
            partner_id = cpo.partner_id.id
            product_tmpl_id = cpol.product_id.product_tmpl_id.id
            psi_ids = psi_obj.search(cr, uid, [('name', '=', partner_id), ('product_id', '=', product_tmpl_id)], context=context)
            psi2unlink += psi_ids
        psi_obj.unlink(cr, uid, psi2unlink, context=context)
        cpol_obj.unlink(cr, uid, ids, context=context)
        return True

    def create_psi(self, cr, uid, ids, context=None):
        psi_obj = self.pool.get("product.supplierinfo")
        cpo_obj = self.pool.get("computed.purchase.order")
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'product', 'product_supplierinfo_form_view')
        res_id = res and res[1] or False
        for cpol in self.browse(cr, uid, ids, context=context):
            cpo = cpol.computed_purchase_order_id
            partner_id = cpo.partner_id.id
            product_tmpl_id = cpol.product_id.product_tmpl_id.id
            
            values = {
                'name': partner_id,
                'product_name': cpol.product_name,
                'product_code': cpol.product_code,
                'product_uom': cpol.uom_po_id.id,
                'package_qty': cpol.package_quantity_inv,
                'min_qty': cpol.package_quantity,
                'product_id': product_tmpl_id,
                'pricelist_ids': [(0, 0, {'min_quantity': 0, 'price': cpol.product_price_inv})],
            }
            psi_id = psi_obj.create(cr, uid, values, context=context)
            cpol.write({'state': 'up_to_date'})
            return psi_id

# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from math import ceil

from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class computed_purchase_order(Model):
    _description="Computed Purchase Order"
    _name = 'computed.purchase.order'
    _order = 'id desc'

    ### Constant Values
    _DEFAULT_NAME = _('New')

    _STATE = [
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    ]

    _target_type = [
        ('product_price_inv', '€'),
        ('time', 'days'),
        ('weight_net', 'kg'),
    ]

    ### Columns section
    def _get_stock_line_ids(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            res[id] = [x.id for x in self.browse(cr, uid, id).line_ids]
        return res


    def _get_computed_amount_duration(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        for cpo in self.browse(cr, uid, ids, context=context):
            min_duration = 999
            amount = 0
            for line in cpo.line_ids:
                if line.average_consumption != 0:
                    duration = (line.computed_qty + line.purchase_qty)/ line.average_consumption
                    min_duration = min(duration, min_duration)
                amount += line.purchase_qty * line.product_price_inv
            res[cpo.id] = {
                'computed_amount': amount, 
                'computed_duration': min_duration,}
        return res


    def _get_products_updated(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        for cpo in self.browse(cr, uid, ids, context=context):
            updated = False
            for line in cpo.line_ids:
                if line.state == 'updated':
                    updated = True
                    break
            res[cpo.id] = updated
        return res


    _columns = {
        'name': fields.char('Computed Purchase Order Reference', size=64, required=True, readonly=True,
            help="Unique number of the automated purchase order, computed automatically when the computed purchase order is created."),
        'company_id': fields.many2one('res.company', 'Company', readonly=True, required=True, 
            help="When you will validate this item, this will create a purchase order for this company."),
        'active': fields.boolean('Active', 
            help="By unchecking the active field, you may hide this item without deleting it."),
        'state': fields.selection(_STATE,'State', required=True,),
        'incoming_date':fields.date('Wished Incoming Date', 
            help="Wished date for products delivery."),
        'partner_id':fields.many2one('res.partner', 'Supplier', required=True,
            domain=[('supplier','=',True)], 
            help="Supplier of the purchase order."),
        'line_ids': fields.one2many('computed.purchase.order.line', 'computed_purchase_order_id', 'Order Lines',
            help="Products to order."),
        'stock_line_ids': fields.function(_get_stock_line_ids, type='one2many', relation='computed.purchase.order.line', help="Products to order."), #this is to be able to display the line_ids on 2 tabs of the view
        'compute_pending_quantity': fields.boolean('Pending quantity taken in account',),
        'compute_draft_quantity': fields.boolean('Draft quantity taken in account',),
        'purchase_order_id': fields.many2one('purchase.order', 'Purchase Order', readonly=True,), 
        'purchase_target': fields.integer("Purchase Target"),
        'target_type': fields.selection(_target_type, 'Target Type', required=True,
            help='''This defines the amount of products you want to purchase. \n 
            The system will compute a purchase order based on the stock you have and the average consumption of each product.
            Target type '€': computed purchase order will cost at least the amount specified 
            Target type 'days': computed purchase order will last at least the number of days specified (according to current average consumption)
            Target type 'kg': computed purchase order will weight at least the weight specified'''),
        'computed_amount': fields.function(_get_computed_amount_duration, 
            type='float', 
            digits_compute=dp.get_precision('Product Price'), 
            string='Amount of the computed order', 
            multi='computed_amount_duration',),
        'computed_duration': fields.function(_get_computed_amount_duration, 
            type='integer', 
            string='Minimum duration after order', 
            multi='computed_amount_duration',),
        'products_updated': fields.function(_get_products_updated, 
            type='boolean', 
            string='Indicate if there were any products updated in the list',),
    }

    ### Defaults section
    _defaults = {
        'name': _DEFAULT_NAME,
        'company_id': lambda s,cr,uid,c: s.pool.get('res.users')._get_company(cr, uid, context=c),
        'active': True,
        'state': 'draft',
        'compute_pending_quantity': True,
        'compute_draft_quantity': True,
        'target_type': 'product_price_inv',
        'purchase_target': 0,
    }

    ### View Section
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        #TODO: create a wizard to validate the change
        vals= {
            'purchase_target': 0, 
            'target_type': 'product_price_inv',
            }
        if partner_id:
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            vals= {
                'purchase_target': partner.purchase_target,
                'target_type': partner.target_type,
                }
        if ids:
            cpo = self.browse(cr, uid, ids, context=context)[0]
            vals['line_ids'] = map(lambda x: (2, x.id, False), cpo.line_ids)
        return {'value': vals}
        

    ### Overload Section
    def create(self, cr, uid, vals, context=None):
        if vals.get('name', self._DEFAULT_NAME) == self._DEFAULT_NAME:
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'computed.purchase.order') or '/'
        order = super(computed_purchase_order, self).create(cr, uid, vals, context=context)
        return order

    def update_sorting(self, cr, uid, values, context=None):
        try:
            if context is None:
                context = {}
            line_ids = values.get('line_ids', False)
            if not line_ids:
                return False

    #        this context check will allow you to change the field list without overriding the whole function
            need_sorting_fields = context.get('need_sorting_fields', False)
            if not need_sorting_fields:
                need_sorting_fields = [
                    'average_consumption',
                    'computed_qty',
                    'stock_duration',
                    'manual_input_output_qty',
                    ]
            for value in line_ids:
                if len(value) > 2 and value[2] and isinstance(value[2], dict) and (set(need_sorting_fields) & set(value[2].keys())):
                    return True
            return False

        except:
            return False

    def write(self, cr, uid, ids, values, context=None):
        if context is None:
            context = {}
        cpo_id = super(computed_purchase_order, self).write(cr, uid, ids, values, context=context)
        if self.update_sorting(cr, uid, values, context=None):
            self._sort_lines(cr, uid, ids, context=context)
        return cpo_id

    ### Private Section
    def _sort_lines(self, cr, uid, ids, context=None):
        cpol_obj = self.pool.get('computed.purchase.order.line')
        if context is None:
            context = {}
        if not isinstance(ids, list):
            ids = [ids]
        for cpo in self.browse(cr, uid, ids, context=context):
            lines = cpol_obj.read(cr, uid, [x.id for x in cpo.line_ids], ['stock_duration', 'average_consumption'], context=context)
            lines = sorted(lines, key=lambda line: line['average_consumption'], reverse=True)
            lines = sorted(lines, key=lambda line: line['stock_duration'])

            id_index_list={}
            for i in lines:
                id_index_list[i['id']] = lines.index(i)
            for line_id in id_index_list.keys():
                cpol_obj.write(cr, uid, line_id, {'sequence': id_index_list[line_id]}, context=context)

    def _make_po_lines(self, cr, uid, id, context=None):
        cpo = self.browse(cr, uid, id, context=context)
        all_lines = []
        for line in cpo.line_ids:
            if line.purchase_qty <> 0:
                line_values={
                    'name': "%s%s" %(line.product_code_inv and '[' + line.product_code_inv + '] ' or '', line.product_name_inv or line.product_id.name_template),
                    'product_qty': line.purchase_qty,
                    'date_planned': cpo.incoming_date or fields.date.context_today(self, cr, uid, context=context),
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_id': line.product_id.id,
                    'price_unit': line.product_price_inv,
                    'taxes_id': [(6, 0, [x.id for x in line.product_id.supplier_taxes_id])],
                }
                all_lines.append((0, 0, line_values),)
        return all_lines


    def _compute_purchase_quantities_days(self, cr, uid, id, context=None):
        cpol_obj = self.pool.get('computed.purchase.order.line')
        cpo = self.browse(cr, uid, id, context=context)
        days = cpo.purchase_target
        for line in cpo.line_ids:
            if line.average_consumption:
                quantity = max(days * line.average_consumption * line.uom_po_id.factor / line.uom_id.factor - line.computed_qty, 0)
                if line.package_quantity and quantity%line.package_quantity:
                    quantity = ceil(quantity / line.package_quantity) * line.package_quantity
            else:
                quantity = line.package_quantity or 0
            cpol_obj.write(cr, uid, line.id, {'purchase_qty': quantity}, context=context)
        return True


    def _compute_purchase_quantities_other(self, cr, uid, id, field = None, context=None):
        cpol_obj = self.pool.get('computed.purchase.order.line')
        cpo = self.browse(cr, uid, id, context=context)
        if not cpo.line_ids:
            return False
        target = cpo.purchase_target
        ok = False
        days = -1
        field_list = cpol_obj.read(cr, uid, [x.id for x in cpo.line_ids], [field], context=context)
        field_list_dict = {}
        for i in field_list:
            field_list_dict[i['id']] = i[field]

        while not ok:
            days +=1
            qty_tmp = {}
            for line in cpo.line_ids:
                if line.average_consumption:
                    quantity = max(days * line.average_consumption * line.uom_po_id.factor / line.uom_id.factor- line.computed_qty, 0)
                    if line.package_quantity and quantity%line.package_quantity:
                        quantity = ceil(quantity / line.package_quantity) * line.package_quantity
                else:
                    quantity = line.package_quantity or 0
                qty_tmp[line.id] = quantity
                
            ok = self._check_purchase_qty(cr, uid, target, field_list_dict, qty_tmp, context=context)
                    
        for line in cpo.line_ids:
            cpol_obj.write(cr, uid, line.id, {'purchase_qty': qty_tmp[line.id]}, context=context)
        return True


    def _check_purchase_qty(self, cr, uid, target = 0, field_list = None, qty_tmp = None, context=None):
        if not target or field_list is None or qty_tmp is None:
            return True
        total = 0
        for key in field_list.keys():
            total += field_list[key] * qty_tmp[key]
        return total >= target


    ### Action section
    def compute_active_product_stock(self, cr, uid, ids, context=None):
        cpol_obj = self.pool.get('computed.purchase.order.line')
        psi_obj = self.pool.get('product.supplierinfo')
        pp_obj = self.pool.get('product.product')
        for cpo in self.browse(cr, uid, ids, context=context):
            cpol_list = []
            # TMP delete all rows, TODO : depends on further request to avoid user data to be lost
            unlink_ids = [cpol.id for cpol in cpo.line_ids]
            cpol_obj.unlink(cr, uid, unlink_ids, context=context)

            # Get product_product and compute stock
            psi_ids = psi_obj.search(cr, uid, [('name', '=', cpo.partner_id.id)], context=context)
            for psi in psi_obj.browse(cr, uid, psi_ids, context=context):
                pp_ids = pp_obj.search(cr, uid, [
                    ('product_tmpl_id', '=', psi.product_id.id),
                    ('state', 'not in', ('end', 'obsolete'))], context=context)
                for pp in pp_obj.browse(cr, uid, pp_ids, context=context):
                    cpol_list.append((0, 0, {
                        'product_id': pp.id,
                        'state': 'up_to_date',
                        'product_code': psi.product_code,
                        'product_name': psi.product_name,
                        'package_quantity': psi.package_qty or psi.min_qty,
                        'average_consumption': pp.average_consumption,
                        'uom_po_id': psi.product_uom.id,
                        }))
            # update line_ids
            self.write(cr, uid, cpo.id, {'line_ids':cpol_list}, context=context)
        return True

    def compute_purchase_quantities(self, cr, uid, id, context=None):
        if isinstance(id, list):
            id = id[0]
        cpo = self.browse(cr, uid, id, context=context)
        if cpo.target_type == 'time':
            res = self._compute_purchase_quantities_days(cr, uid, id, context=context)
        else:
            res = self._compute_purchase_quantities_other(cr, uid, id, field = cpo.target_type, context=context)
        return res


    def make_order(self, cr, uid, id, context=None):
        if isinstance(id, list):
            id = id[0]
        po_lines = self._make_po_lines(cr, uid, id, context=context)
        if not po_lines:
            raise osv.except_osv(_('Invalid Action!'), _('All purchase quantities are set to 0!'))

        cpo = self.browse(cr, uid, id, context=context)
        po_obj = self.pool.get('purchase.order')
        partner_obj = self.pool.get('res.partner')
        partner = partner_obj.browse(cr, uid, cpo.partner_id.id, context=context)
        po_values = {
            'origin': cpo.name,
            'partner_id': cpo.partner_id.id,
            'location_id': self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.partner_id.property_stock_customer.id, 
            'pricelist_id': partner.property_product_pricelist_purchase.id,
            'order_line': po_lines,
        }
        po_id = po_obj.create(cr, uid, po_values, context=context)
        self.write(cr, uid, id, {'state': 'done', 'purchase_order_id': po_id}, context=context)

        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'purchase', 'purchase_order_form')
        res_id = res and res[1] or False
        return {
            'name': _('Purchase Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': po_id or False,
        }

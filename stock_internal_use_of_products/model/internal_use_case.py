# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class internal_use_case(Model):
    _name = "internal.use.case"
    _description = "Case of Internal Uses"

    ### Columns Section
    _columns = {
        'name': fields.char('Name', size=64, required=True,),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'location_from': fields.many2one('stock.location', 'Origin Location', required=True, domain="[('usage','=','internal')]"),
        'location_to': fields.many2one('stock.location', 'Destination Location', required=True,),
        'expense_account': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Expense Account",
            view_load=True, 
            required=True),
        'active': fields.boolean('Active', help="By unchecking the active field, you may hide an INCOTERM without deleting it."),
        'journal': fields.many2one('account.journal', 'Journal', required=True, ),
    
    }
    ### Defaults section
    _defaults = {
        'company_id': lambda s,cr,uid,c: s.pool.get('res.users')._get_company(cr, uid, context=c),
        'active': True,
    }

    ### Constraints Section
    def _check_company_id(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if (iuc.company_id.id != iuc.location_from.company_id.id or
                    iuc.company_id.id != iuc.location_to.company_id.id) :
                return False
        return True

    def _check_different_location_ids(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if iuc.location_from.id == iuc.location_to.id :
                return False
        return True

    def _check_location_usages(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if (iuc.location_from.usage == 'view' or
                    iuc.location_to.usage == 'view') :
                return False
        return True

    _constraints = [
        (_check_company_id, 'Error: Origin location and Destination Location must belong to the company.', 
            ['location_from', 'location_to', 'company_id', ]),
        (_check_different_location_ids, 'Error: Origin location and Destination Location must be different.', 
            ['location_from', 'location_to',]),
        (_check_location_usages, 'Error: Origin location and Destination Location can not be of \'view\' type.', 
            ['location_from', 'location_to',]),
    ]
    

    _sql_constraints = [('name_company_id_uniq','unique(name,company_id)', 'Case of Internal uses name must be unique by company!')]

    ### Overload Section
    def copy_data(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'name': '%s (copy)' %(self.browse(cr, uid, id, context=context).name)
        })
        return super(internal_use_case, self).copy_data(cr, uid, id, default, context=context)

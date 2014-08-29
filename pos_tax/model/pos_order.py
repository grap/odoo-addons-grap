# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class pos_order(osv.osv):
    _inherit = "pos.order"
    
    def compute_group_tax(self, cr, uid, cur, line, group_tax,
                                                current_company, context=None):
        account_tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')

        taxes = []
        for ptri in line.pol_tax_rel_id:
            if ptri.tax_id.company_id.id == current_company.id:
                taxes.append(ptri.tax_id)

        computed_taxes = account_tax_obj.compute_all(cr, uid, taxes,
                line.price_unit * (100.0-line.discount) / 100.0,
                line.qty)['taxes']

        tax_amount = 0
        for tax in computed_taxes:
            tax_amount += cur_obj.round(cr, uid, cur, tax['amount'])
            group_key = self._get_tax_key(cr, uid, tax, context=context)
            group_tax.setdefault(group_key, 0)
            group_tax[group_key] += cur_obj.round(cr, uid, cur, tax['amount'])
        return (computed_taxes, group_tax, tax_amount)

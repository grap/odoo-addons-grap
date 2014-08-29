# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class stock_inventory(osv.osv):
    _inherit = 'stock.inventory'

    _columns = {
        'set_account_zero': fields.boolean("Set account valuation to zero",help="If checked, the balance of the inventory account will be reseted to 0 after validating the inventory"),
    }

    #Overwrite section
    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_inventory, self).action_done(cr, uid, ids, context=context)

        set_zero = any(si.set_account_zero is True for si in self.browse(cr, uid, ids, context=context))

        if set_zero:
            #create move lines
            self._reset_stock_account(cr, uid, ids, context=context)
        return res

    #Private section
    def _reset_stock_account(self, cr, uid, ids, context=None):
        ip_obj = self.pool.get('ir.property')
        aa_obj = self.pool.get('account.account')
        am_obj = self.pool.get('account.move')
        ap_obj = self.pool.get('account.period')

        inventory = self.browse(cr, uid, ids, context=context)
        inventory = inventory and inventory[0] or False

        #get the stock accounts and journal
        stock_journal = ip_obj.get(cr, uid,
            'property_stock_journal',
            'product.category', context=context)
        if not stock_journal:
            return False

        valuation_account = ip_obj.get(cr, uid,
            'property_stock_valuation_account_id',
            'product.category', context=context)
        if not valuation_account:
            return False

        #get the balance
        balance = valuation_account.balance

        period = ap_obj.find(cr, uid, dt=inventory.date, context=context)
        period = period and period[0] or False

        if balance < 0:
            input_account = ip_obj.get(cr, uid,
                'property_stock_account_input',
                'product.template', context=context)
            if not input_account:
                input_account = ip_obj.get(cr, uid,
                    'property_stock_account_input_categ',
                    'product.category', context=context)
            if not input_account:
                return False
            
            #compute account_move_lines
            debit_line_vals = {
                        'name': "reset %s" % inventory.name,
                        'ref': "reset account valuation for %s" % inventory.name,
                        'date': inventory.date,
                        'debit': -balance,
                        'account_id': valuation_account.id,
                        'period_id': period,
            }
            credit_line_vals = {
                        'name': "reset %s" % inventory.name,
                        'ref': "reset account valuation for %s" % inventory.name,
                        'date': inventory.date,
                        'credit': -balance,
                        'account_id': input_account.id,
                        'period_id': period,
            }
            
        elif balance > 0:
            output_account = ip_obj.get(cr, uid,
                'property_stock_account_output',
                'product.template', context=context)
            if not output_account:
                output_account = ip_obj.get(cr, uid,
                    'property_stock_account_output_categ',
                    'product.category', context=context)
            if not output_account:
                return False
        
            #compute account_move_lines
            debit_line_vals = {
                        'name': "reset %s" % inventory.name,
                        'ref': "reset account valuation for %s" % inventory.name,
                        'date': inventory.date,
                        'debit': balance,
                        'account_id': output_account.id,
                        'period_id': period,
            }
            credit_line_vals = {
                        'name': "reset %s" % inventory.name,
                        'ref': "reset account valuation for %s" % inventory.name,
                        'date': inventory.date,
                        'credit': balance,
                        'account_id': valuation_account.id,
                        'period_id': period,
            }
        
        else:
            return False
            
        #create account_move
        am_obj.create(cr, uid,
                {
                 'journal_id': stock_journal.id,
                 'date': inventory.date,
                 'period_id': period,
                 'line_id': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)],
                 'ref': "reset %s" % inventory.name}, context=context
             )

# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.tools.translate import _

class account_move(Model):
    _inherit = 'account.move'
    
    def rename_account_move_change_number(self, cr, uid, ids, context = None):
        for id in ids:
            old_account_move = self.browse(cr, uid, id, context=context)
            old_name = old_account_move.name
            old_narration = old_account_move.narration or ''
            # unpost acount move
            self.button_cancel(cr, uid, [id], context=context)

            # set name to "/"
            self.write(cr, uid, [id], {'name': '/'}, context = context)
            
            # post account move
            self.post(cr, uid, [id], context=context)
            new_name = self.browse(cr, uid, id, context=context).name
            
            # Add description of the change
            self.write(cr, uid, [id], {
                'narration': old_narration + _("\nAccount move renamed old name : %s ; new name : %s" ) % (old_name,new_name,)
                }, context = context)
        return True
    

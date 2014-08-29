# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields
from openerp.osv.orm import Model

class account_move(Model):
    _inherit = 'account.move'

    ### Columns section
    _columns = {
        'merged_move_quantity': fields.integer('Quantity of merged moves', readonly=True),
        'merged_narration': fields.text('Notes about merged accound moves', readonly=True),
    }

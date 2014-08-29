# -*- coding: utf-8 -*-

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.tools.translate import _

class res_country_state(Model):
    _inherit = 'res.country.state'

    _columns = {
        'code': fields.char('State Code', size=4, required=True,),
    }

# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields

class pos_order_line(Model):
    _inherit="pos.order.line"
    _columns = {
        'state': fields.related('order_id', 'state', type='char', string='State'),
    }

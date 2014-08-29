# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields

class grap_ethiquette_type(Model):
    _description='Ethiquette Type'
    _name = 'grap.ethiquette.type'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly="1"),
        'name': fields.char('Type Name', required=True, size=64),
        'ethiquette_color': fields.char('Color', required=True, size=7, help="Color of the type of ethiquette. Format #RRGGBB" ),
    }

    _defaults = {
        'company_id': lambda s,cr,uid,c: s.pool.get('res.users')._get_company(cr, uid, context=c),
    }

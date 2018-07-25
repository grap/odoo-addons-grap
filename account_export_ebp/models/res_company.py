# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class res_company(Model):
    """Add parameters to export accounting moves to EBP's software"""
    _inherit = 'res.company'

    # Columns section
    def _get_ebp_trigram(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for rc in self.browse(cr, uid, ids, context=context):
            if rc.fiscal_type in ['fiscal_child', 'fiscal_mother']:
                res[rc.id] = rc.code
            else:
                res[rc.id] = ''
        return res

    _columns = {
        'ebp_trigram': fields.function(
            _get_ebp_trigram, type='char', string='EBP Trigram', store=True),
        'ebp_uri': fields.char(
            'EBP Share URI', size=256,
            help="""The URI of the network share containing the company's"""
            """ EBP folder. Format: smb://SERVER/SHARE/DIR"""),
        'ebp_domain': fields.char(
            'EBP User Domain', size=256,
            help="""The domain of the user to access the company's EBP"""
            """ folder."""),
        'ebp_username': fields.char(
            'EBP User Name', size=256,
            help="""The name of the user to access the company's EBP"""
            """ folder."""),
        'ebp_password': fields.char(
            'EBP User Password', size=256,
            help="""The password of the user to access the company's"""
            """ EBP folder."""),
    }

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields
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

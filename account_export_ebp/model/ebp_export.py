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

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _

class ebp_export(Model):
    _name = "ebp.export"

    def _get_name(self, cr, uid, ids, name, args, context):
        if context is None:
            context = {}
        res={}
        for id in ids:
            res[id] = 'export_' + str(id)
        return res

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True,
            help="The company this fiscal year belongs to."),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal year', required=True,),
        'exported_moves': fields.integer("Number of moves exported", readonly = True),
        'ignored_moves': fields.integer("Number of moves ignored", readonly = True,),
        'exported_lines': fields.integer("Number of lines exported", readonly = True),
        'exported_accounts': fields.integer("Number of accounts exported", readonly = True),
        'exported_moves_ids': fields.one2many('account.move', 'exported_ebp_id', 'Exported Moves'),
        'data_moves': fields.binary('Moves file', readonly=True),
        'data_accounts': fields.binary('Accounts file', readonly=True),
        'data_balance': fields.binary('Balance file', readonly=True),
        'date': fields.date('Date', required=True),
        'name': fields.function(_get_name, 'Name', type='char', store=True)
    }
    _defaults = {
        'exported_moves': lambda * a: 0,
        'ignored_moves': lambda * a: 0,
        'exported_lines': lambda * a: 0,
        'exported_accounts': lambda * a: 0,
        'date': lambda * a: fields.date.today()
    }

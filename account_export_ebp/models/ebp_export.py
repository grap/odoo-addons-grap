# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class ebp_export(Model):
    _name = "ebp.export"

    def _get_name(self, cr, uid, ids, name, args, context):
        return {x: 'export_' + str(x) for x in ids}

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True),
        'fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Fiscal year', required=True, readonly=True),
        'exported_moves': fields.integer(
            'Number of moves exported', readonly=True),
        'ignored_moves': fields.integer(
            'Number of moves ignored', readonly=True),
        'exported_lines': fields.integer(
            'Number of lines exported', readonly=True),
        'exported_accounts': fields.integer(
            'Number of accounts exported', readonly=True),
        'exported_moves_ids': fields.one2many(
            'account.move', 'exported_ebp_id', 'Exported Moves',
            readonly=True),
        'data_moves': fields.binary(
            'Moves file', readonly=True),
        'data_accounts': fields.binary(
            'Accounts file', readonly=True),
        'data_balance': fields.binary(
            'Balance file', readonly=True),
        'date': fields.date(
            'Date', required=True, readonly=True),
        'name': fields.function(
            _get_name, 'Name', type='char', store=True, readonly=True),
        'description': fields.text(
            'Description', readonly=True,
            help="Extra Description for Accountant Manager."),
    }
    _defaults = {
        'exported_moves': lambda * a: 0,
        'ignored_moves': lambda * a: 0,
        'exported_lines': lambda * a: 0,
        'exported_accounts': lambda * a: 0,
        'date': lambda * a: fields.date.today()
    }

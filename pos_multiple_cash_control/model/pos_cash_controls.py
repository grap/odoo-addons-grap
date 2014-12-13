# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>)
#    Some modification has been realized by GRAP:
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.addons import decimal_precision as dp


class pos_cash_controls(Model):
    _name = 'pos.cash.controls'
    _order = 'id desc'

    _columns = {
        'pos_session_id': fields.many2one(
            'pos.session', 'Session', select=1),
        'journal_id': fields.many2one(
            'account.journal', 'Journal', select=1),
        'cash_register_id': fields.many2one(
            'account.bank.statement', 'Cash Register', select=1),
        'opening_total': fields.related(
            'cash_register_id', 'balance_start', type='float',
            digits_compute=dp.get_precision('Account'),
            string="Starting Balance",
            help="Computed using the cash control at the opening.",
            readonly=True),
        'opening_details_ids': fields.related(
            'cash_register_id', 'opening_details_ids',
            type='one2many', relation='account.cashbox.line',
            string='Opening Cash Control'),
        'closing_total': fields.related(
            'cash_register_id', 'balance_end_real', type='float',
            digits_compute=dp.get_precision('Account'),
            string="Ending Balance",
            help="Computed using the cash control lines",
            readonly=True),
        'details_ids': fields.related(
            'cash_register_id', 'details_ids',
            type='one2many', relation='account.cashbox.line',
            string='Cash Control'),
        'state': fields.related(
            'pos_session_id', 'state',
            type='char', string='State'),
    }

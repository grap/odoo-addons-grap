# -*- coding: utf-8 -*-
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.addons import decimal_precision as dp

#class PosCashControl(models.Model):
#    _name = 'pos.cash.control'
#    _order = 'journal_id'

#    # Column Section
#    session_id = fields.Many2one(
#        comodel_name='pos.session', string='Session', select=True)

#    journal_id = fields.Many2one(
#        comodel_name='account.journal', string='Journal', select=1),

###    _columns = {

###        'cash_register_id': fields.many2one(
###            'account.bank.statement', 'Cash Register', select=1),
###        'opening_total': fields.related(
###            'cash_register_id', 'balance_start', type='float',
###            digits_compute=dp.get_precision('Account'),
###            string="Starting Balance",
###            help="Computed using the cash control at the opening.",
###            readonly=True),
###        'opening_details_ids': fields.related(
###            'cash_register_id', 'opening_details_ids',
###            type='one2many', relation='account.cashbox.line',
###            string='Opening Cash Control'),
###        'closing_total': fields.related(
###            'cash_register_id', 'balance_end_real', type='float',
###            digits_compute=dp.get_precision('Account'),
###            string="Ending Balance",
###            help="Computed using the cash control lines",
###            readonly=True),
###        'details_ids': fields.related(
###            'cash_register_id', 'details_ids',
###            type='one2many', relation='account.cashbox.line',
###            string='Cash Control'),
###        'state': fields.related(
###            'pos_session_id', 'state',
###            type='char', string='State'),
###    }

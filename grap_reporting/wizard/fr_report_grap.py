# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Reporting Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import Model
from openerp.osv import fields


class account_sig_report(Model):
    _name = 'account.sig.report'
    _description = 'French SIG report'

    _columns = {
        'period_ids': fields.many2many(
            'account.period', 'account_sig_report_period_rel',
            'report_id', 'period_id', required=True),
        'date_start': fields.date(
            'Start Date', required=False),
        'date_stop': fields.date(
            'End Date', required=False),
    }

    def print_sig_report(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', [])
        data = {}
        data['form'] = {}
        data['ids'] = active_ids
        data['form']['date_start'] = self.browse(cr, uid, ids)[0].date_start
        data['form']['date_stop'] = self.browse(cr, uid, ids)[0].date_stop
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n.fr.sig',
            'datas': data}


class account_treso_report(Model):
    _name = 'account.treso.report'
    _description = 'Tresorerie'

    _columns = {
        'period_ids': fields.many2many(
            'account.period',
            'account_treso_report_period_rel',
            'report_id',
            'period_id',
            required=True,),
        'date_start': fields.date(
            'Start Date',
            required=False,
        ),
        'date_stop': fields.date(
            'End Date',
            required=False,
        ),
    }

    def print_treso_report(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', [])
        data = {}
        data['form'] = {}
        data['ids'] = active_ids
        data['form']['date_start'] = self.browse(cr, uid, ids)[0].date_start
        data['form']['date_stop'] = self.browse(cr, uid, ids)[0].date_stop
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n.fr.treso',
            'datas': data}

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Move - Date and Ceriod Conform Module for Odoo
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


class account_move(Model):
    _inherit = 'account.move'

    def _get_period_from_date_company_id(
            self, cr, uid, date, company_id, context=None):
        if not context:
            context = {}
        ctx = context.copy()
        ctx.update({
            'company_id': company_id,
            'account_period_prefer_normal': True})
        return self.pool.get('account.period').find(
            cr, uid, date, context=ctx)[0]

    def onchange_date_company_journal(
            self, cr, uid, ids, date, company_id, journal_id, context=None):
        if not company_id or not date or not journal_id:
            return {}
        if self.pool.get('account.journal').browse(
                cr, uid, journal_id, context=context).allow_date:
            period_id = self._get_period_from_date_company_id(
                cr, uid, date, company_id, context=context)
            return {'value': {'period_id': period_id}}
        else:
            return {}

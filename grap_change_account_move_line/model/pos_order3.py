# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Account Move Lines Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import Model


class pos_order(Model):
    _inherit = 'pos.order'

    def compute_group_tax(
            self, cr, uid, cur, line, group_tax, current_company,
            context=None):
        account_tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')

        taxes = []
        for ptri in line.pol_tax_rel_id:
            if ptri.tax_id.company_id.id == current_company.id:
                taxes.append(ptri.tax_id)

        computed_taxes = account_tax_obj.compute_all(
            cr, uid, taxes, line.price_unit * (100.0 - line.discount) / 100.0,
            line.qty)['taxes']

        tax_amount = 0
        for tax in computed_taxes:
            tax_amount += cur_obj.round(cr, uid, cur, tax['amount'])
            group_key = self._get_tax_key(cr, uid, tax, context=context)
            group_tax.setdefault(group_key, 0)
            group_tax[group_key] += cur_obj.round(cr, uid, cur, tax['amount'])
        return (computed_taxes, group_tax, tax_amount)

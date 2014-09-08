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

from openerp.osv import fields, osv


class pos_config(osv.osv):
    _inherit = 'pos.config'

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True),
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c: self.pool.get('res.users').browse(
                cr, uid, uid, c).company_id.id),
    }

    def _check_cash_control(self, cr, uid, ids, context=None):
        return True

    _constraints = [
        (
            _check_cash_control,
            "You cannot have two cash controls in one Point Of Sale !",
            ['journal_ids']),
    ]

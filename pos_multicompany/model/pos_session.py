# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multi Company Context module for OpenERP
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


class pos_session(Model):
    _inherit = 'pos.session'

    _columns = {
        'company_id': fields.related(
            'config_id', 'company_id', type='many2one', relation='res.company',
            string='Company', store=True, readonly=True, required=False)
    }

    def _default_company(self, cr, uid, context=None):
        res = self.pool.get('pos.config').search(cr, uid, [])
        if res:
            config = self.pool.get('pos.config').browse(cr, uid, res[0])
            return config.company_id.id
        else:
            return False

    _defaults = {
        'company_id': _default_company,
    }

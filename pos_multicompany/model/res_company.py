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

from openerp.osv.orm import Model


class res_company(Model):
    _inherit = 'res.company'

    def create(self, cr, uid, values, context=None):
        """ Create default pos_category for the new company"""
        pc_obj = self.pool['pos.category']
        id = super(res_company, self).create(cr, uid, values, context=context)
        pc_obj._create_pos_categ_for_company(cr, uid, id, context=context)
        return id

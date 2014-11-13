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


class product_product(Model):
    _inherit = 'product.product'

    def default_get(self, cr, uid, fields, context=None):
        """This function remove an hard-coded and invalid default value
        for pos_categ_id"""
        context.pop('default_pos_categ_id', None)
        return super(product_product, self).default_get(
            cr, uid, fields, context=context)

    # Erase Section
    def _get_default_pos_categ_id(self, cr, uid, context=None):
        """The default category is now managed by the field 'is_default'
        this function do NOT call super(pos_category, self)."""
        rc_obj = self.pool['res.company']
        pc_obj = self.pool['pos.category']
        rc_id = rc_obj._company_default_get(
            cr, uid, 'pos.category', context=context)
        return pc_obj._get_pos_categ_id_by_company(
            cr, uid, rc_id, context=context)

    _defaults = {
        'pos_categ_id': _get_default_pos_categ_id,
    }

    # Constraints section
    def _check_pos_categ_id_company_id(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if pp.company_id and pp.pos_categ_id:
                if pp.company_id.id != pp.pos_categ_id.company_id.id:
                    return False
        return True

    _constraints = [
        (_check_pos_categ_id_company_id,
            """You can not affect a pos category that does not belong to the"""
            """ company of the product !""",
            ['company_id', 'pos_categ_id']),
    ]

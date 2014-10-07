# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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
from openerp.osv.orm import TransientModel


class wizard_change_product_category(TransientModel):
    """Wizard to allow to change the eShop Category of products."""
    _name = 'wizard.change.product.category'

    def change_product_category(self, cr, uid, ids, context=None):
        pp_obj = self.pool['product.product']
        for wcpc in self.browse(cr, uid, ids, context=context):
            pp_ids = [x.id for x in wcpc.old_eshop_category_id.product_ids]
            pp_obj.write(cr, uid, pp_ids, {
                'eshop_category_id': wcpc.new_eshop_category_id.id},
                context=context)
        return {}

    _columns = {
        'old_eshop_category_id': fields.many2one(
            'eshop.category', 'Old eShop Category', required=True,
            readonly=True),
        'new_eshop_category_id': fields.many2one(
            'eshop.category', 'New eShop Category', required=True,
            domain="""[('id', '!=', old_eshop_category_id)]"""),
    }

    _defaults = {
        'old_eshop_category_id': lambda self, cr, uid, ctx: ctx and ctx.get(
            'active_id', False) or False
    }

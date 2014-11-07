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

import logging

from openerp import SUPERUSER_ID
from openerp.osv import fields
from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class pos_category(Model):
    _inherit = 'pos.category'

    # Custom Section
    def _get_pos_categ_id_by_company(self, cr, uid, company_id, context=None):
        res = self.search(cr, uid, [
            ('is_default', '=', True), ('company_id', '=', company_id)])
        return res and res[0] or False

    def _create_pos_categ_for_company(self, cr, uid, company_id, context=None):
        vals = {
            'name': _('Others'),
            'is_default': True,
            'company_id': company_id}
        self.create(cr, uid, vals, context=context)

    # Column Section
    _columns = {
        'is_default': fields.boolean(
            'Is Default', readonly=True,
            help="""Set it to true if you want to put it by default for"""
            """ the current company."""),
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True),
    }

    # Constraints section
    def _check_is_default_company_id(self, cr, uid, ids, context=None):
        is_default = []
        pc_ids = self.search(cr, uid, [('is_default', '=', True)])
        for pc in self.browse(cr, uid, pc_ids, context=context):
            if pc.is_default:
                if pc.company_id in is_default:
                    return False
                else:
                    is_default.append(pc.company_id)
        return True

    _constraints = [
        (
            _check_is_default_company_id,
            'There is only one default pos category by company!',
            ['is_default', 'company_id']),
    ]

    # Default Section
    def _get_default_company_id(self, cr, uid, context=None):
        rc_obj = self.pool['res.company']
        return rc_obj._company_default_get(
            cr, uid, 'pos.category', context=context)

    _defaults = {
        'company_id': _get_default_company_id,
    }

    # Init Section
    def init(self, cr):
        """On init the module, Create a default pos category 'other'
        for each company that don't have any default pos_category;
        Reaffect products of pos category whose company id does'nt match
        with product category to the default new pos category."""
        uid = SUPERUSER_ID
        imd_obj = self.pool['ir.model.data']
        rc_obj = self.pool['res.company']

        # get all default pos_category
        pc_ids = self.search(cr, uid, [('is_default', '=', True)])
        pc_res = self.read(cr, uid, pc_ids, ['company_id'])
        rc_with_ids = [temp['company_id'][0] for temp in pc_res]

        # get all company without default pos_category
        rc_without_ids = rc_obj.search(
            cr, uid, [('id', 'not in', rc_with_ids)])
        base_rc_id = imd_obj.get_object_reference(
            cr, uid, 'base', 'main_company')[1]

        # in this state, xml/yml files is not analyzed, so we update default
        # pos category by this way. Otherwise, the script, will create a
        # pos_category for base.main_company instead of using the
        # point_of_sale.categ_others object, raising a constraint Error after.
        if base_rc_id in rc_without_ids:
            base_pc_id = imd_obj.get_object_reference(
                cr, uid, 'point_of_sale', 'categ_others')[1]
            vals = {
                'is_default': True,
                'company_id': base_rc_id}
            self.write(cr, uid, [base_pc_id], vals)
            rc_without_ids.remove(base_rc_id)

        # Create default pos_categories
        for rc_id in rc_without_ids:
            _logger.info("Create Default POS Category for company `%d`." % (
                rc_id))
            self._create_pos_categ_for_company(cr, uid, rc_id)

        # Get all new or existing default pos category
        pc_ids = self.search(cr, uid, [('is_default', '=', True)])
        pc_res = self.read(cr, uid, pc_ids, ['company_id'])
        pc_rc_list = {}
        for temp in pc_res:
            pc_rc_list[temp['company_id'][0]] = temp['id']

        # Reaffect product to the correct product default category
        cr.execute("""
            SELECT pp.id AS pp_id,
                pt.company_id AS pp_company_id,
                pc.company_id AS pc_company_id
            FROM product_product AS pp
            INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
            INNER JOIN pos_category pc ON pp.pos_categ_id = pc.id
            WHERE pt.company_id != pc.company_id""")
        for cursor in cr.fetchall():
            _logger.info("Update Product `%d`. Set pos category to `%d`." % (
                cursor[0], pc_rc_list[cursor[1]]))
            cr.execute("""
            UPDATE product_product
            SET pos_categ_id = %s
            WHERE id = %s""", (
                pc_rc_list[cursor[1]],
                cursor[0]))

    # Overload Section
    def unlink(self, cr, uid, ids, context=None, check=True):
        """Refuse to delete default pos categories.
        Reaffect product linked to a unlinked pos_category to the default
        pos category of the company of the product (if exist)"""
        pp_obj = self.pool['product.product']
        # Check if there are default categories
        pc_ids = self.search(
            cr, uid, [('is_default', '=', True), ('id', 'in', ids)])
        if pc_ids:
            pc_list = self.browse(cr, uid, pc_ids, context=context)
            raise osv.except_osv(
                _('Default Point of Sale Category!'),
                _('You cannot delete this categories: %s!') % (
                    ', '.join([pc.name for pc in pc_list])))

        # Change product category to the default category if possible
        pp_ids = pp_obj.search(cr, uid, [
            ('pos_categ_id', 'in', ids), ('company_id', '!=', False)])
        for pp in pp_obj.browse(cr, uid, pp_ids, context=context):
            vals = {
                'pos_categ_id': self._get_pos_categ_id_by_company(
                    cr, uid, pp.company_id.id, context=context)}
            pp_obj.write(cr, uid, [pp.id], vals, context=context)

        return super(pos_category, self).unlink(cr, uid, ids, context)

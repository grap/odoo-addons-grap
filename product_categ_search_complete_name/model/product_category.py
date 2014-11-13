# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Search On Complete Category Name Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


class product_category(Model):
    _inherit = 'product.category'
    _rec_name = 'complete_name'

    def name_search(
            self, cr, uid, name='', args=None, operator='ilike', context=None,
            limit=80):
        ids = []
        ids = self.search(cr, uid, [
            ('complete_name', operator, name)] + args,
            limit=limit, context=context)
        return self.name_get(cr, uid, ids)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for pc in self.browse(cr, uid, ids):
            res.append((pc.id, pc.complete_name))
        return res

    def _compute_complete_name(self, cr, uid, pId, context=None):
        pc = self.browse(cr, uid, pId, context=context)
        if pc.parent_id:
            res = self._compute_complete_name(
                cr, uid, pc.parent_id.id, context=context) + ' / ' + pc.name
        else:
            res = pc.name
        return res

    def _get_complete_name(self, cr, uid, ids, pFields, args, context=None):
        res = []
        for pc in self.browse(cr, uid, ids, context=context):
            res.append((pc.id, self._compute_complete_name(
                cr, uid, pc.id, context=context)))
        return dict(res)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        assert False

    # Columns section
    _columns = {
        'complete_name': fields.function(
            _get_complete_name, type='char', string='Name', store=True, ),
    }

    def write(self, cr, uid, ids, values, context=None):
        res = super(product_category, self).write(
            cr, uid, ids, values, context=context)
        for pc in self.browse(cr, uid, ids, context=context):
            for pc_child in pc.child_id:
                self.write(cr, uid, [pc_child.id], {
                    'complete_name': self._compute_complete_name(
                        cr, uid, pc_child.id, context=context)
                }, context=context)
        return res

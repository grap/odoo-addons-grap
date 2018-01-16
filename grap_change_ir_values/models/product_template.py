# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class product_template(Model):
    _inherit = 'product.template'

    def _get_uom_id(self, cr, uid, *args):
        if args[0].get('install_mode', False):
            return super(product_template, self)._get_uom_id(
                cr, uid, *args)
        else:
            return False

    _defaults = {
        'uom_id': _get_uom_id,
        'uom_po_id': _get_uom_id,
    }

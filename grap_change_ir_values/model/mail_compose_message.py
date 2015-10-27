# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Ir Values Module for Odoo
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

from lxml import etree

from openerp.osv.orm import setup_modifiers
from openerp.osv.orm import Model


class mail_compose_message(Model):
    _inherit = 'mail.compose.message'

    def default_get(self, cr, uid, fields, context=None):
        """set no default value for template_id"""
        res = super(mail_compose_message, self).default_get(
            cr, uid, fields, context=context)
        res.pop('template_id', False)
        return res

    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        context = context and context or {}
        res = super(mail_compose_message, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='template_id']")
            if nodes:
                nodes[0].set('required', '1')
                setup_modifiers(nodes[0], res['fields']['template_id'])
                res['arch'] = etree.tostring(doc)
        return res

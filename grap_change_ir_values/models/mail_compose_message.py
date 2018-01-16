# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

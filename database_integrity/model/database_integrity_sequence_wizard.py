# -*- encoding: utf-8 -*-
##############################################################################
#
#    Database Integrity module for OpenERP
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields
#from openerp.osv import osv
from openerp.exceptions import AccessError
from openerp.tools.translate import _

class database_integrity_sequence_wizard(TransientModel):
    _name = 'database.integrity.sequence.wizard'

    def fix_invalid_sequence(self, cr, uid, ids, context=None):
        if self.pool['res.users'].has_group(cr, uid, 'base.group_system'):
            for disw in self.browse(cr, uid, ids, context=context):
                for diswl in disw.line_ids:
                    if diswl.state == 'invalid':
                        cr.execute("ALTER SEQUENCE %s RESTART WITH %s;" % (
                            diswl.sequence_name, diswl.max_id))
            return True
        else:
            # We check in this way because TransientModel doesn't accept
            # ir_model_access definition.
            raise AccessError(
                _('You have to belong to administration group.'))

    def default_get(self, cr, uid, fields, context=None):
        res = super(database_integrity_sequence_wizard, self).default_get(
            cr, uid, fields, context=context)
        res['line_ids'] = []
        correct_line_ids = []
        cr.execute("""
            SELECT
                c.relname as table_name,
                substring(pg_get_serial_sequence(c.relname, a.attname)
                    from length(ns.nspname) +2) AS sequence_name,
                a.attname as field_name
            FROM pg_catalog.pg_attribute a
            INNER JOIN pg_catalog.pg_class c ON c.oid=a.attrelid
            LEFT JOIN pg_catalog.pg_namespace ns ON ns.oid = c.relnamespace
            WHERE a.attnum >0
            AND NOT a.attisdropped
            AND NOT pg_get_serial_sequence(c.relname, a.attname) IS NULL
            AND c.relkind='r'
            AND ns.nspname NOT IN ('information_schema', 'pg_catalog')
            ORDER BY c.relname;""")
        cr1_all = cr.fetchall()
        for cr1 in cr1_all:
            cr.execute("""
                SELECT
                    (SELECT last_value FROM %s) sequence_value,
                    (SELECT max(%s) FROM %s) max_id;""" % (
                cr1[1], cr1[2], cr1[0]))
            cr2 = cr.fetchone()
            vals = (0, 0, {
                'table_name': cr1[0],
                'sequence_name': cr1[1],
                'field_name': cr1[2],
                'sequence_value': cr2[0],
                'max_id': cr2[1] or 0})
            if cr2[1] and cr2[1] > cr2[0]:
                vals[2]['state'] = 'invalid'
                res['line_ids'].append(vals)
            else:
                vals[2]['state'] = 'valid'
                correct_line_ids.append(vals)
        res['line_ids'] += correct_line_ids
        return res

    _columns = {
        'line_ids': fields.one2many(
            'database.integrity.sequence.wizard.line', 'wizard_id',
            'All Sequences'),
    }

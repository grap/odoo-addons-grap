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


class database_integrity_sequence_wizard_line(TransientModel):
    _name = "database.integrity.sequence.wizard.line"

    _STATE = [('valid', 'Valid'), ('invalid', 'Invalid')]

    _columns = {
        'wizard_id': fields.many2one(
            'database.integrity.sequence.wizard',
            'Wizard Reference', readonly=True),
        'table_name': fields.char('Table Name', readonly=True, required=True),
        'sequence_name': fields.char(
            'Sequence Name', readonly=True, required=True),
        'field_name': fields.char('Field Name', readonly=True, required=True),
        'max_id': fields.integer('Max ID', readonly=True, required=True),
        'sequence_value': fields.integer(
            'Sequence Value', readonly=True, required=True),
        'state': fields.selection(_STATE, string='Status'),
    }

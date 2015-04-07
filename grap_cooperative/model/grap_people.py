# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Cooperative module for Odoo
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
from openerp.osv.orm import Model


class grap_people(Model):
    _description = 'People'
    _name = 'grap.people'
    _inherits = {'grap.member': 'grap_member_id'}
    _order = 'last_name,first_name'

    # Fields Function section
    def _get_name(self, firstName, lastName):
        return lastName + ' ' + firstName

    # Column section
    _columns = {
        'grap_member_id': fields.many2one(
            'grap.member', 'Member', required=True, ondelete="cascade"),
        'first_name': fields.char(
            'First name', size=128, required=True),
        'last_name': fields.char(
            'Last name', size=128, required=True),
        'private_phone': fields.char(
            'Private Phone', size=64),
        'activity_ids': fields.one2many(
            'grap.activity.people', 'people_id', 'Activities'),
        'accountant_activity_ids': fields.one2many(
            'grap.activity', 'accountant_interlocutor_id',
            'Accounting Performed for Activities'),
        'hr_activity_ids': fields.one2many(
            'grap.activity', 'hr_interlocutor_id',
            'Human Ressources Performed for Activities'),
        'attendant_activity_ids': fields.one2many(
            'grap.activity', 'attendant_interlocutor_id',
            'Attending Performed for Activities'),
        'mandate_ids': fields.many2many(
            'grap.mandate', 'grap_people_mandate_rel',
            'people_id', 'mandate_id', 'Mandates',),
        'description': fields.text('Self Description'),
        'skills': fields.text('Skills'),
        'catchword': fields.char('Catchword'),

    }

    # Overloads section
    def create(self, cr, uid, data, context=None):
        data['name'] = self._get_name(data['first_name'], data['last_name'])
        return super(grap_people, self).create(cr, uid, data, context=context)

    def write(self, cr, uid, ids, data, context=None):
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        if 'last_name' in data.keys() and 'first_name' in data.keys():
            # global change
            data['name'] = self._get_name(
                data['first_name'], data['last_name'])
        elif 'last_name' in data.keys():
            # specific change for each people
            for people in self.browse(cr, uid, ids, context=context):
                spec_data = {'name': self._get_name(
                    people.first_name, data['last_name'])}
                super(grap_people, self).write(
                    cr, uid, people.id, spec_data, context=context)
        elif 'first_name' in data.keys():
            # specific change for each people
            for people in self.browse(cr, uid, ids, context=context):
                spec_data = {'name': self._get_name(
                    data['first_name'], people.last_name)}
                super(grap_people, self).write(
                    cr, uid, people.id, spec_data, context=context)
        return super(grap_people, self).write(
            cr, uid, ids, data, context=context)

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields

logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
except ImportError:
    logger.debug("account_export_ebp - 'unidecode' librairy not found")


class account_add_suffix(TransientModel):
    _name = "account.add.suffix"

    _columns = {
        'line_ids': fields.one2many(
            'account.add.suffix.line', 'account_add_suffix_id',
            'Add Suffix Lines'),
    }

    # View Section
    def affect_suffix(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        rp_obj = self.pool.get('res.partner')

        for suf in self.browse(cr, uid, ids, context=context):
            for line in suf.line_ids:
                if line.suffix:
                    rp_obj.write(cr, uid, [line.partner_id.id], {
                        'ref_nb': line.suffix,
                    }, context=context)
        return True

    # Overloading section
    def default_get(self, cr, uid, pFields, context=None):
        rp_obj = self.pool.get('res.partner')
        line_ids = []
        res = super(account_add_suffix, self).default_get(
            cr, uid, pFields, context=context)

        partner_ids = context.get('active_ids', False)
        if not partner_ids:
            return res
        existing_suffixes = {}
        sql_req = """
            SELECT rp.company_id, rp.ref_nb from res_partner rp
            WHERE ref_nb is not Null """
        cr.execute(sql_req)
        result = cr.dictfetchall()
        for item in result:
            existing_suffixes.setdefault(item['company_id'], [])
            existing_suffixes[item['company_id']] += [item['ref_nb']]

        for partner in rp_obj.browse(cr, uid, partner_ids, context=context):
            if partner.ref_nb:
                suffix = partner.ref_nb
            else:
                suffix = self._get_suffix(
                    partner.name, existing_suffixes.get(
                        partner.company_id.id, []))
                if suffix:
                    existing_suffixes.setdefault(partner.company_id.id, [])
                    existing_suffixes[partner.company_id.id] += [suffix]
            line_ids.append((0, 0, {
                'partner_id': partner.id,
                'company_id': partner.company_id.id,
                'suffix': suffix,
            }))
            res.update({'line_ids': line_ids})
        return res

    # Private Section
    def _get_suffix(self, name, existing_suffixes):
        # remove special caracters
        name2 = ''.join(e for e in name if e.isalnum())
        # if nothing remains, return False
        if not name2:
            return False
        # first try: return the 4 fisrt caracters
        suffix = name2[:min(4, len(name2))].upper()
        suffix = unidecode.unidecode(suffix)
        if suffix and not(suffix in existing_suffixes):
            return suffix
        # second try: look for different words in the name
        # and try taking caracters from them
        for sep in [' ', """'""", '-']:
            if sep in name:
                names = name.split(sep)
                for i in range(0, len(names)):
                    names[i] = ''.join(e for e in names[i] if e.isalnum())
                for j in range(1, len(names)):
                    for n in range(3, 0, -1):
                        if len(names[0]) >= n:
                            suffix = (
                                names[0][:n].upper() +
                                names[j][:(4 - n)].upper())
                            suffix = unidecode.unidecode(suffix)
                            if suffix and not(suffix in existing_suffixes):
                                return suffix
#        third try: takes first 3 caracters and add a one digit number
        for x in range(2, 10):
            suffix = name2[:min(3, len(name2))].upper() + str(x)
            suffix = unidecode.unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
#        fourth try: takes first 2 caracters and add a two digit number
        for x in range(10, 100):
            suffix = name2[:min(2, len(name2))].upper() + str(x)
            suffix = unidecode.unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
#        fifth try: takes first 1 caracters and add a three digit number
        for x in range(100, 1000):
            suffix = name2[:1].upper() + str(x)
            suffix = unidecode.unidecode(suffix)
            if suffix and not(suffix in existing_suffixes):
                return suffix
        return False


class account_add_suffix_line(TransientModel):
    _name = "account.add.suffix.line"

    _columns = {
        'account_add_suffix_id': fields.many2one(
            'account.add.suffix', 'Add Suffix Id'),
        'partner_id': fields.many2one(
            'res.partner', 'Partner'),
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'suffix': fields.char(
            'Suggested EBP Suffix', size=4),
    }

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

from openerp.osv import fields
from openerp.osv.orm import Model


class account_tax_code(Model):
    _inherit = 'account.tax.code'

    def _get_nb_moves(self, cr, uid, ids, name, arg, context=None):
        res = {}
        aml_obj = self.pool.get('account.move.line')
        for aId in ids:
            aml_ids = aml_obj.search(cr, uid, [
                ('tax_code_id', '=', aId), ('date', '>=', '01/12/2012')],
                context=context)
            res[aId] = len(aml_ids)
        return res

    def _search_nb_moves(self, cr, uid, obj, name, args, context=None):
        if not args:
            return []
        query, query_args = self._get_search_moves_query(
            cr, uid, args, overdue_only=False, context=context)
        cr.execute(query, query_args)
        res = cr.fetchall()
        if not res:
            return [('id', '=', '0')]
        return [('id', 'in', [x[0] for x in res])]

    # Columns section
    _columns = {
        'ref_nb': fields.char(
            'Tax Code\'s Account suffix in EBP', size=4,
            help="""When exporting Entries to EBP, this suffix will be"""
            """ appended to the Account Number to make it a new Account."""),
        'nb_moves': fields.function(
            _get_nb_moves, string='Number of moves',
            fnct_search=_search_nb_moves, type='integer',
            help="Number of account moves for this tax code"),
    }

    # Private section
    def _get_search_moves_query(
            self, cr, uid, args, overdue_only=False, context=None):
        having_where_clause = ' AND '.join(
            map(lambda x: '(COUNT(*) %s %%s)' % (x[1]), args))
        having_values = [x[2] for x in args]
        return "SELECT tax_code_id, count(*) \
            FROM account_move_line \
            WHERE date >= '01/12/2012' \
            GROUP BY tax_code_id \
            HAVING " + having_where_clause, having_values

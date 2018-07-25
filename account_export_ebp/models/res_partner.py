# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class res_partner(Model):
    _inherit = 'res.partner'

    # Columns section
    def _nb_moves(self, cr, uid, ids, name, arg, context=None):
        res = {}
        aml_obj = self.pool.get('account.move.line')
        for aId in ids:
            aml_ids = aml_obj.search(cr, uid, [
                ('partner_id', '=', aId), ('date', '>=', '01/12/2012')],
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

    _columns = {
        # Partner's account number in EBP
        'ref_nb': fields.char(
            'Partner\'s Account suffix in EBP',
            help="""When exporting Entries to EBP, this suffix will be"""
            """ appended to the Account Number to make it a Partner"""
            """ Account."""),
        'nb_moves': fields.function(
            _nb_moves, string='Number of moves',
            fnct_search=_search_nb_moves, type='integer',
            help="Number of account moves for this partner"),
    }

    # Constraints section
    _sql_constraints = [
        (
            'partner_suffix_uniq',
            'unique (ref_nb, company_id)',
            'The partner suffix must be unique per company!')
    ]

    # Overloading section
    def write(self, cr, uid, ids, vals, context=None):
        ref_nb = vals.get('ref_nb', False)
        if ref_nb:
            vals['ref_nb'] = ref_nb.upper()
        return super(res_partner, self).write(
            cr, uid, ids, vals, context=context)

    # Private section
    def _get_search_moves_query(
            self, cr, uid, args, overdue_only=False, context=None):
        having_where_clause = ' AND '.join(
            map(lambda x: '(COUNT(*) %s %%s)' % (x[1]), args))
        having_values = [x[2] for x in args]
        return """
            SELECT partner_id, count(*)
            FROM account_move_line
            WHERE date >= '01/12/2012'
            GROUP BY partner_id
            HAVING """ + having_where_clause, having_values

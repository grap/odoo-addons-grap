# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Columns section
    ebp_suffix = fields.Char(
        string="Suffix in EBP", oldname="ref_nb",
        help="When exporting Entries to EBP, this suffix will be"
        " appended to the Account Number to make it a Partner Account.")

    move_line_qty = fields.Integer(
        compute='_compute_move_line_qty',
        string='Quantity of Account Move Lines',
        help="Number of account moves for this partner")

    # Columns section
    @api.multi
    def _compute_move_line_qty(self):
        AccountMoveLine = self.env['account.move.line']
        # for aId in ids:
            # aml_ids = aml_obj.search(cr, uid, [
                # ('partner_id', '=', aId), ('date', '>=', '01/12/2012')],
                # context=context)
            # res[aId] = len(aml_ids)
        # return res
        # TODO
# 
#    Search Section
    # def _search_ean_duplicates_exist(self, operator, operand):
        # products = self.search([])
        # res = products._get_ean_duplicates()
        # if operator == '=' and operand is True:
            # product_ids = res.keys()
        # elif operator == '=' and operand is False:
            # product_ids = list(set(products.ids) - set(res.keys()))
        # else:
            # raise UserError(_(
                # "Operator '%s' not implemented.") % (operator))
        # return [('id', 'in', product_ids)]
# 
# 
    # def _search_move_line_qty(self, cr, uid, obj, name, args, context=None):
        # if not args:
            # return []
        # query, query_args = self._get_search_moves_query(
            # cr, uid, args, overdue_only=False, context=context)
        # cr.execute(query, query_args)
        # res = cr.fetchall()
        # if not res:
            # return [('id', '=', '0')]
        # return [('id', 'in', [x[0] for x in res])]
# 
    # _columns = {
        # Partner's account number in EBP
# 
    # }
# 
    # Constraints section
    # _sql_constraints = [
        # (
            # 'partner_suffix_uniq',
            # 'unique (ref_nb, company_id)',
            # 'The partner suffix must be unique per company!')
    # ]
# 
    # Overloading section
    # def write(self, cr, uid, ids, vals, context=None):
        # ref_nb = vals.get('ref_nb', False)
        # if ref_nb:
            # vals['ref_nb'] = ref_nb.upper()
        # return super(res_partner, self).write(
            # cr, uid, ids, vals, context=context)
# 
    # Private section
    # def _get_search_moves_query(
            # self, cr, uid, args, overdue_only=False, context=None):
        # having_where_clause = ' AND '.join(
            # map(lambda x: '(COUNT(*) %s %%s)' % (x[1]), args))
        # having_values = [x[2] for x in args]
        # return """
            # SELECT partner_id, count(*)
            # FROM account_move_line
            # WHERE date >= '01/12/2012'
            # GROUP BY partner_id
            # HAVING """ + having_where_clause, having_values

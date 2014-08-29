# -*- encoding: utf-8 -*-
###############################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
###############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import string


class product_product(Model):
    _inherit = 'product.product'

    ### Constant Values
    _SEPARATOR = ':'
    _REPLACEMENT = ''

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            unaccent = get_unaccent_wrapper(cr)
            self.check_access_rights(cr, uid, 'read')
            where_query = self._where_calc(cr, uid, args, context=context)
            self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            if "product_product__product_tmpl_id" not in from_clause:
                from_clause += ",\"product_template\" as \"product_product__product_tmpl_id\""
            if operator in ('ilike', 'like'):
                percent = True
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            names = name.split(self._SEPARATOR)
            pwc = ""
            for n in names:
                search_name = '%%%s%%' % n if percent else n
                pwc += """ AND ({display_name} {operator} {percent})
                """.format(operator=operator, percent=unaccent('%s'),
                display_name=unaccent('product_product__product_tmpl_id.name'))
                where_clause_params += [search_name]
            pwc = pwc[5:]

            query = """SELECT product_product.id
                         FROM {from_clause}
                      {where} ({pwc})
                     ORDER BY {display_name}
                    """.format(from_clause=from_clause, where=where_str, pwc=pwc, 
                               display_name=unaccent('product_product__product_tmpl_id.name'))

            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)

            cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], cr.fetchall())

            if ids:
                return self.name_get(cr, uid, ids, context)
            else:
                return []
        return super(product_product,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
                context=None, count=False):
        try:
            args2 = args
            for arg in args2:
                if isinstance(arg, (tuple, list)):
                    if isinstance(arg[2], (str, unicode)) and \
                            self._SEPARATOR in arg[2]:
                        criterias = arg[2].split(self._SEPARATOR)
                        new_arg_tmp = [(arg[0], arg[1], x) for x in criterias]
                        l = len(new_arg_tmp) - 1
                        init_string = ['&'] * l
                        new_arg = init_string + new_arg_tmp
                        args.remove(arg)
                        args += new_arg
        except:
            pass
        return super(product_product, self).search(cr, uid, args,
                offset=offset, limit=limit, order=order, context=context,
                count=count)

    def _replace_separator(self, cr, uid, ids=None, context=None):
        product_ids = super(product_product, self)\
            .search(cr, SUPERUSER_ID,
                [('name', 'like', '%' + self._SEPARATOR + '%')],
                context=context)
        for product in self.browse(cr, SUPERUSER_ID, product_ids,
                                    context=context):
            new_name = string.replace(product.name, self._SEPARATOR,
                                      self._REPLACEMENT)
            self.write(cr, SUPERUSER_ID, product.id, {'name': new_name},
                        context=context)
        return product_ids

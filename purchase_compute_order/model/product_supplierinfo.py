# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import fields
from openerp.osv.orm import Model

class product_supplierinfo(Model):
    _inherit = 'product.supplierinfo'

    ### SQL Constraints section
    _sql_constraints = [
        ('psi_product_name_uniq','unique(name,product_id)', 'You cannot register several times the same supplier on a product!'),
    ]

    ### Private section
    def _delete_duplicates(self, cr, uid, ids=None, context=None):
        query = """
            SELECT pp.id
            FROM
                product_supplierinfo psi 
                INNER JOIN product_template pt ON psi.product_id = pt.id
                INNER JOIN product_product pp ON pp.product_tmpl_id = pt.id
            GROUP BY
                pp.id, psi.name
            HAVING
                count(*) > 1"""
        cr.execute(query)
        product_ids = map(lambda x:x[0], cr.fetchall())
        products = self.pool.get('product.product').browse(cr, uid, product_ids, context=context)

        deleted_ids = []
        for product in products:
            delete = False
            for psi in product.seller_ids:
                if delete:
                    deleted_ids.append(psi.id)
                    psi.unlink()
                else:
                    delete = True
        return deleted_ids

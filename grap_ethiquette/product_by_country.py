# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import tools

class product_by_country(Model):
    _name="product.by.country"
    _description="Product by country"
    _auto = False
    _log_access = False
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'country_id': fields.many2one('res.country', 'Country', readonly=True),
        'quantity': fields.integer('Number of product', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'product_by_country')
        cr.execute("""
CREATE OR REPLACE VIEW product_by_country as (
    SELECT 
        row_number() OVER (ORDER BY product_template.company_id, product_product.ethiquette_origin_country) AS id, 
        product_template.company_id as company_id, 
        product_product.ethiquette_origin_country as country_id, 
        count(*) as quantity
    FROM product_product
    INNER JOIN product_template
        on product_template.id = product_product.product_tmpl_id
    LEFT OUTER JOIN res_country 
        ON res_country.id = product_product.ethiquette_origin_country
    WHERE product_product.active = True
        AND product_template.company_id is not null
    GROUP BY 
        product_product.ethiquette_origin_country, 
        product_template.company_id
)""")

# -*- coding: utf-8 -*-

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import tools

class product_by_department(Model):
    _name="product.by.department"
    _description="Product by department"
    _auto = False
    _log_access = False
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'department_id': fields.many2one('res.country.department', 'Department', readonly=True),
        'state_id': fields.many2one('res.country.state', 'State', readonly=True),
        'country_id': fields.many2one('res.country', 'Country', readonly=True),
        'quantity': fields.integer('Number of product', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'product_by_department')
        cr.execute("""
CREATE OR REPLACE VIEW product_by_department as (
    SELECT 
        row_number() OVER (ORDER BY product_template.company_id, product_product.ethiquette_origin_department) AS id, 
        product_template.company_id as company_id, 
        product_product.ethiquette_origin_department as department_id, 
        res_country_state.id as state_id,
        res_country.id as country_id,
        count(*) as quantity
    FROM product_product
    INNER JOIN product_template
        on product_template.id = product_product.product_tmpl_id
    LEFT OUTER JOIN res_country_department
        ON res_country_department.id = product_product.ethiquette_origin_department
    LEFT OUTER JOIN res_country_state
        ON res_country_department.country_state_id = res_country_state.id
    inner join res_country
        ON product_product.ethiquette_origin_country = res_country.id
    WHERE product_product.active = True
        AND product_template.company_id is not null
    GROUP BY 
        product_product.ethiquette_origin_department, 
        product_template.company_id,
        res_country_state.id,
        res_country.id
)""")

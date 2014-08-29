# -*- encoding: utf-8 -*-
###############################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
###############################################################################

import time
import datetime
from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _


class product_product(Model):
    _inherit = "product.product"

    def _min_date(self, cr, uid, product_id, context=None):
        query = """SELECT to_char(min(date), 'YYYY-MM-DD') \
                from stock_move where product_id = %s""" % (product_id)
        cr.execute(query)
        results = cr.fetchall()
        return results and results[0] and results[0][0] \
                or time.strftime('%Y-%m-%d')

    def _average_consumption(self, cr, uid, ids, fields, arg, context=None):
        result = {}
        stock_move_obj = self.pool.get('stock.move')
        total_consumption = 0
        first_date = time.strftime('%Y-%m-%d')
        begin_date = (datetime.datetime.today()
                    - datetime.timedelta(days=365))\
                    .strftime('%Y-%m-%d')

        if context is None:
            context = {}
        c = context.copy()
        c.update({
            'states': ('confirmed', 'waiting', 'assigned', 'done'),
            'what': ('out', ),
            'from_date': begin_date
            })
        stock = self.get_product_available(cr, uid, ids, context=c)

        for product in self.browse(cr, uid, ids, context=context):
            first_date = max(
                begin_date,
                self._min_date(cr, uid, product.id, context=c)
                )
            nb_days = (
                    datetime.datetime.today()
                    - datetime.datetime.strptime(first_date, '%Y-%m-%d')
                    ).days
            result[product.id] = {
                'average_consumption': nb_days
                                    and - stock[product.id] / nb_days
                                    or False,
                'total_consumption': - stock[product.id] or False,
                'nb_days': nb_days or False,
            }
        return result

    _columns = {
        'average_consumption': fields.function(_average_consumption,
            type='float', string='Average Consumption per day',
            multi="average_consumption"),
        'total_consumption': fields.function(_average_consumption,
            type='float', string='Total Consumption',
            multi="average_consumption"),
        'nb_days': fields.function(_average_consumption,
            type='float', string='Number of days for the calculation',
            multi="average_consumption",
            help="The calculation will be done for the last 365 days or since \
            the first purchase or sale of the product if it's more recent"),
    }

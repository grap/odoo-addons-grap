# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model

class account_invoice(Model):
    _inherit = 'account.invoice'

    def inv_line_characteristic_hashcode(self, invoice, invoice_line):
        """We override this function to group lines regardless of the product_id. 
        Lines having the same hashcode will be grouped together if the journal has the 'group line' option. """
        return "%s-%s-%s-%s"%(
            invoice_line['account_id'],
            invoice_line.get('tax_code_id',"False"),
            invoice_line.get('analytic_account_id',"False"),
            invoice_line.get('date_maturity',"False"))

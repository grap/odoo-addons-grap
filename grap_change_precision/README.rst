.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================================
GRAP Custom - Change the precisions names and values of some fields
===================================================================


* Add a new precision 'GRAP Purchase Unit Price', used in:
    * account_invoice_line.price_unit
    * pricelist_partnerinfo.price
    * product_template.standard_price
    * purchase_order_line.price_unit
    * stock_move.unit_price


* Add a new precision 'GRAP Purchase Unit Discount', used in:
    * account_invoice_line.discount


* Change Precision to 'Product UoS' for the following fields:
    * pos_order_line.qty


Roadmap / Issues
----------------

* TODO : set to 'GRAP Purchase Unit Price' the following fields:
    * product_template.standard_price_vat_included

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)

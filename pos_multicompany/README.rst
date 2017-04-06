.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Point of Sale Settings in Multi company context
===============================================


Change the point of sale module for Multi company context.

Functionality
-------------

* Add a 'company_id' related fields on 'pos_config' and 'pos_session'
  objects and restrict access right;
* Add a new field 'company_id' on 'pos_category' objects and new
  constraint on product_product to force a product to be linked to a
  pos_category that belong to the same company;
* OpenERP create a default pos_category 'Others' for products;
  This module will create pos_category 'Others' for each company;
  This pos_category will be the new default value;
  (So add a field 'is_default' on pos_category that must be uniq
  by company)
* It is forbidden to delete default pos_category

Remark and limits
-----------------

* This module is interesting only if you design you multicompany
  with products that belong to a defined company.
  Otherwise, if you have 'gobal' products, the pos_category
  will not be available for this products;
* this module give read access to all user, to avoid ACL error, if user
  want to create a product and don't belong to POS user Group;




.. figure:: ./stock_inventory_valuation/static/description/stock_inventory_form.png
   :width: 800px

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)

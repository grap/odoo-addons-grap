.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
GRAP - Change Ir Values
=======================

Set ir.values for default feature

Partners (res.partner)
----------------------

* Partners receive mail by default:
    * field : 'notification_email_send';
    * value : 'comment';

Products (product.template)
---------------------------

* Products has no default UoM:
    * field : 'uom_id';
    * value : False;
* Products has no default Purchase UoM:
    * field : 'uom_po_id';
    * value : False;
* Products has Null Produce Delay:
    * field : 'produce_delay';
    * value : 0;
* Products has Null Sale Delay:
    * field : 'sale_delay';
    * value : 0;

Technical Information:
----------------------

* for product_template.uom_id and uom_po_id, a special test is done to
  know if creation come from the load of a new module. In that special
  case, default value is unchanged;

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>

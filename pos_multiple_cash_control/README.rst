.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Allow the cash control on all cash registers for a session
==========================================================

Functionnality
--------------

* Disable constrains on number of journals with cash control enabled,
  on pos config.

    * Add extra functionnality on pos_session:
        * It's now allowed to control all the payment method when user
    open or close his session;

TODO:
-----
    * description;
    * test;

--> MOVE THIS FEATURE IN ANOTHER MODULE
    * Add extra constraint on product if income_pdt or expense_pdt:
        * This product are manage by account manager only;
        * this product must have account_income (or account_expense);
        * This product must have only one VAT (if expense_pdt);
        * this product can not be 'sale_ok' or 'purchase_ok';

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)

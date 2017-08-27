.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
Point Of Sale - Change Payment Move lines
=========================================

this module intents to manage correctly payment move lines generated from
point of sale.

By default, with Odoo, an account move is create by payment, that generates
a lot of useless account moves for an accountant.

With this module, when closing a PoS session, an account move is created for
each combination of: 
- pos order partner (*)
- account (counterpart account)
- pos order date (without time, just date)

(*) : Note that if a pos order is associated to a partner, without an invoice,
the partner is ignored, reducing more move quantity.

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (www.grap.coop)

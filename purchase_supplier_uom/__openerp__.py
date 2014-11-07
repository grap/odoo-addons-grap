# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase - Supplier UOM Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Purchase - Supplier UOM',
    'version': '2.1',
    'category': 'Purchase',
    'description': """
Allow user to define the supplier uom for a product
===================================================

Functionnality :
----------------
In product_supplierinfo, replace the fields.related by a fields.many2one.
For inheritance matters, we don't directly replace the field (if you replace
a not-stored field with a stored one, you'll get problems at each update) but
we modify it into a fields.function that sets and gets a new fields.many2one.

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
        'purchase',
    ],
    'data': [
        'view/view.xml',
        'data/function.xml',
    ],
}

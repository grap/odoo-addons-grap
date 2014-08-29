# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Unique Default Code module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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
    'name': 'Product - Unique Default Code',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
The field reference (default_code) of a product is readonly, unique & computed
==============================================================================

Features:
---------
The field (default_code) of a product :
    * become **readonly** and **unique** ;
    * is composed by a prefix depending of the product's company and"""
    """ product's category and a unique id (new fields);

Technical Information:
----------------------
    * After installing this module, please fill correctly the field"""
    """product_code_prefix in both table 'res_company' and product_category';

Example:
--------
    * If prefix of the company is "COM";
    * If prefix of the category is "CAT";
        * the prefix of the first product of the category for the company"""
    """ will be COM-CAT-0001.

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
    * Author : Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'view/product_view.xml',
        'view/res_company_view.xml',
    ],
    'demo': [
        'demo/res_company.xml',
    ],
}

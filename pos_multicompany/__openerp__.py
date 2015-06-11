# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multi Company Context module for OpenERP
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
    'name': 'Point Of Sale - Multi Company Context',
    'version': '0.2',
    'summary': 'Change Point of Sale for Multi company context',
    'category': 'Point of Sale',
    'description': """
Change the point of sale module for Multi company context
=========================================================

Functionality:
--------------
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

Remark and limits:
------------------
    * This module is interesting only if you design you multicompany
      with products that belong to a defined company.
      Otherwise, if you have 'gobal' products, the pos_category
      will not be available for this products;
    * this module give read access to all user, to avoid ACL error, if user
      want to create a product and don't belong to POS user Group;

History:
--------
    * This module is a merge of :
        'pos_config_multi';
        'grap_pos_category_multi';

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2013, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir_rule.yml',
        'security/ir_model_access.yml',
        'view/view.xml',
    ],
}

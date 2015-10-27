# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Ir Values Module for Odoo
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
    'name': 'GRAP - Change Ir Values',
    'version': '1.0',
    'category': 'GRAP - Custom',
    'description': """
Set ir.values for default feature
=================================

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

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2013-Today, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'depends': [
        'mail',
        'email_template',
        'product',
    ],
    'data': [
        'data/ir_values.yml',
    ],
}

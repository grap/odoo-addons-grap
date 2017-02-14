# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Improve Images module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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
    'name': 'Point of Sale - Improve Images',
    'summary': 'Improvements on Display of products and categories images',
    'version': '1.0',
    'category': 'Point Of Sale',
    'description': """
Improvements on Display of products and categories images in Point of Sale
==========================================================================

Technical information:
----------------------
    * Increase speed:
        * Products:
            * Uses image_medium instead of image;
            * Load image only if product has one;
        * Categories:
            * Uses image_medium instead of image (new field);
    * Increase display:
        * If product has no image, the display of the product is changed,
          (Size of the name is increased for better visibility);

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'css': [
        'static/src/css/pii.css',
    ],
    'js': [
        'static/src/js/pii.js',
    ],
    'installable': False,
}

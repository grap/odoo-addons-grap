# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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
    'name': 'Sale - Recovery Moment',
    'version': '0.1',
    'summary': """Manage Recovery Moments and Places for Sale Order""",
    'category': 'Sale',
    'description': """
Manage Recovery Moments and Places for Sale Order
=================================================

Functionality:
--------------
    * XXX;

Technical Information:
----------------------
    * XXX;

TODO:
-----
    * Possibility to create a moment group based on existing moment group,
    by sliding by a number of days;
    * maybe a link on stock.picking.out better;
    * make the link between stock.picking and moment group by sale_id;
    * finish color management for kanban view;
    * make company_id a related field on both moment and moment group object;

    * Make demo data for stock;
    * Realize some test;
    * fr translation;
    * ir access;
    * ir rules;
    * ir group;

Technical Limits:
    * This module displays some Total or sale Order; This amount will be wrong
    in a multicurrencies context for the instance;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock',
    ],
    'data': [
        'data/ir_sequence_type.yml',
        'data/ir_sequence.yml',
        'view/action.xml',
        'view/view.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/sale_recovery_place.yml',
        'demo/sale_recovery_moment_group.yml',
        'demo/sale_recovery_moment.yml',
        'demo/sale_order.yml',
    ],
    'css': [
        'static/src/css/css.css',
    ],
    'images': [
    ],
}

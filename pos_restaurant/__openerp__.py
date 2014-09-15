# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Restaurant module for OpenERP
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
    'name': 'Point of Sale - Restaurant',
    'version': '0.2',
    'category': 'Sale',
    'description': """
Add extra informations for restaurant
=====================================
Features :
----------
    * Add a model 'pos.table' managed in point_of_sale configuration menu;
    * Add a field table_id on pos_order;
    * Possibility to select table in back-office view and tactile view;

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
        'pos_second_header',
    ],
    'demo': [
        'demo/pos_table.yml',
        'demo/sale_shop.yml',
    ],
    'data': [
        'security/ir_rule.yml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'view/view.xml',
        'view/action.xml',
        'view/view_agregate.xml',
        'view/action_agregate.xml',
        'view/menu.xml',
    ],
    'qweb': [
        'static/src/xml/pr.xml',
    ],
    'js': [
        'static/src/js/pr.js',
    ],
    'css': [
        'static/src/css/pr.css',
    ],
    'images': [
        'static/src/img/screenshots/covers_daily_evolution.png',
        'static/src/img/screenshots/covers_monthly_evolution.png',
        'static/src/img/screenshots/covers_weekly_distribution.png',
        'static/src/img/screenshots/covers_weekly_evolution.png',
    ],
}

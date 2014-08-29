# -*- coding: utf-8 -*-
{
    'name': 'GRAP - Remove default product uom',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Product : sets default uom and purchase uom to None
===================================================
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        #'point_of_sale',
    ],
    'init_xml': [],
    'update_xml': [
        #'point_of_sale_view.xml',
    ],
    'demo_xml': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': True,
    'complexity': "easy",
    'installable': True,
    'auto_install': False,
}

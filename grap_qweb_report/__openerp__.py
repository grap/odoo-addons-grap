# -*- coding: utf-8 -*-
{
    'name': 'GRAP - Custom Qweb Reports',
    'version': '8.0.1.0.0',
    'category': 'GRAP - Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'report', # TMP
        'report_webkit',
        'base_fiscal_company',
    ],
    'data': [
        'report/qweb_template_layout.xml',
        'report/qweb_template_sale_order.xml',
        'report/ir_actions_report_xml.xml',
    ],
}

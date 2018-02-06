# -*- coding: utf-8 -*-
{
    'name': 'GRAP - Custom Qweb Reports',
    'version': '8.0.1.0.0',
    'category': 'GRAP - Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'purchase',
        'sale',
        'l10n_fr_siret',
        'base_fiscal_company',
        'sale_food',
    ],
    'data': [
        'report/qweb_template_layout.xml',
        'report/qweb_template_sale_order.xml',
        'report/qweb_template_purchase_order.xml',
        'report/qweb_template_purchase_order_quotation.xml',
        'report/qweb_template_account_invoice.xml',
        'report/ir_actions_report_xml.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
}

# -*- coding: utf-8 -*-

{
    'name': 'GRAP - Reporting',
    'version': '2.X',
    'category': 'Accounting & Finance',
    'description': """
Correct & Add financial reports.
================================
    * Correct of l10n_fr "Balance Sheet" and "Profit & loss" reports ; 
    * provide "IOR" report (Interim Operating Results) ; 
    * provide "CF" report (Cash Flow) ; 
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_fiscal_company',
        'l10n_fr',
    ],
    'init_xml': [
    ],
    'demo_xml': [],
    'update_xml': [
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "wizard/fr_report_compute_grap_view.xml",
        "report/grap_report_lines.xml",
    ],
    'installable': True,
    'application': True,
}

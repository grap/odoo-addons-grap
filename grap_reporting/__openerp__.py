# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Reporting Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
    'name': 'GRAP - Reporting',
    'version': '2.5',
    'category': 'Accounting & Finance',
    'description': """
Correct & Add financial reports
===============================

* Correct of l10n_fr "Balance Sheet" and "Profit & loss" reports;
* provide "IOR" report (Interim Operating Results);
* provide "CF" report (Cash Flow);

TODO MIGRATION
--------------

* remove obsolete reporting;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_fiscal_company',
        'l10n_fr',
    ],
    'data': [
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "wizard/fr_report_compute_grap_view.xml",
        "report/grap_report_lines.xml",
    ],
    'installable': False,
}

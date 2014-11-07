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

from grap_reporting.report import grap_base_report
from report import report_sxw


class treso(grap_base_report.grap_base_report):
    def __init__(self, cr, uid, name, context):
        super(treso, self).__init__(cr, uid, name, context)

report_sxw.report_sxw(
    'report.l10n.fr.treso', 'account.move.line',
    'addons/grap_reporting/report/compute_treso.rml',
    parser=treso, header=False)

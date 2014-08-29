# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from grap_reporting.report import grap_base_report
from report import report_sxw


class treso(grap_base_report.grap_base_report):
    def __init__(self, cr, uid, name, context):
        super(treso, self).__init__(cr, uid, name, context)

report_sxw.report_sxw('report.l10n.fr.treso', 'account.move.line','addons/grap_reporting/report/compute_treso.rml', parser=treso, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

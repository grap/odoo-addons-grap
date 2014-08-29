# -*- coding: utf-8 -*-
import time
from report import report_sxw

class report_webkit_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        # updating product to update edition_state to the value 'OK'
        cr.execute("update product_product set ethiquette_edition_state=0 where id in (select product_id from grap_ethiquette_print_wizard_line where wizard_id = %s)" %(context['active_id']))
        super(report_webkit_html, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.grap.ethiquette.report.html',
    'grap.ethiquette.print.wizard', 
    'addons/grap_ethiquette/report/grap_ethiquette_report_html.mako',
    parser=report_webkit_html)


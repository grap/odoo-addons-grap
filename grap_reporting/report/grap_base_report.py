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

from l10n_fr.report import base_report
import time
from datetime import datetime


class grap_base_report(base_report.base_report):
    def __init__(self, cr, uid, name, context):
        super(grap_base_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            '_set_pourcentage': self._set_pourcentage,
            '_pourcentage': self._pourcentage,
            '_dates': self._dates,
        })

    def _load(self, name, form):
        date_start = form['date_start']
        date_stop = form['date_stop']
        self._set_variable('date_start', date_start)
        self._set_variable('date_stop', date_stop)

        self.cr.execute("""
        SELECT l10n_fr_line.code,definition
        FROM l10n_fr_line
        LEFT JOIN l10n_fr_report
            ON l10n_fr_report.id=report_id
        WHERE l10n_fr_report.code=%s""", (name))
        datas = self.cr.dictfetchall()
        for line in datas:
            self._load_accounts(
                form, line['code'], eval(line['definition']),
                date_start=date_start, date_stop=date_stop)

    def _load_accounts(
            self, form, code, definition, fiscalyear=None, date_start=False,
            date_stop=False):
        accounts = {}
        for x in definition['load']:
            p = x.split(":")
            accounts[p[1]] = [p[0], p[2]]
        aSum = 0.0
        query_params = []
        query_cond = "("
        for account in accounts:
            query_cond += "aa.code LIKE '" + account + "%%' OR "
        query_cond = query_cond[:-4] + ")"

        if len(definition['except']) > 0:
            query_cond = query_cond + " and ("
            for account in definition['except']:
                query_cond += "aa.code NOT LIKE '" + account + "%%' AND "
            query_cond = query_cond[:-5] + ")"

        company_obj = self.pool.get('res.company')
        user_obj = self.pool.get('res.users')
        company = user_obj.browse(
            self.cr, self.uid, self.uid).company_id.id
        company_ids = company_obj.search(
            self.cr, self.uid, [('fiscal_company', '=', company)])
        if company not in company_ids:
            company_ids.append(company)
        company_cond = " AND aml.company_id = ANY(%s)"
        query_params.append(list(company_ids))

        query = """
            SELECT
                aa.code AS code, SUM(debit) as debit,
                SUM(credit) as credit
            FROM account_move_line aml
            LEFT JOIN account_account aa ON aa.id=aml.account_id
            LEFT JOIN account_move am ON aml.move_id = am.id WHERE
            """ + query_cond + company_cond + " AND aml.state='valid'"
        if date_start:
            query = query + " AND am.date >= %s"
            query_params.append(date_start)
        if date_stop:
            query = query + " AND am.date <= %s"
            query_params.append(date_stop)
        query = query + " GROUP BY code"
        self.cr.execute(query, query_params)

        lines = self.cr.dictfetchall()
        for line in lines:
            for account in accounts:
                if(line["code"].startswith(account)):
                    operator = accounts[account][0]
                    aType = accounts[account][1]
                    value = 0.0
                    if(aType == "S"):
                        value = line["debit"] - line["credit"]
                    elif(aType == "D"):
                        value = line["debit"] - line["credit"]
                        if(value < 0.001):
                            value = 0.0
                    elif(aType == "C"):
                        value = line["credit"] - line["debit"]
                        if(value < 0.001):
                            value = 0.0
                    if(operator == '+'):
                        aSum += value
                    else:
                        aSum -= value
                    break
        self._set_variable(code, aSum)

    def _set_pourcentage(self, variable, num, den):
        if den == 0:
            valeur = ""
        else:
            valeur = "{0:.0f}%".format(float(num) / den * 100)
        self._set_variable(variable, valeur)

    def _dates(self, date_start, date_stop):
        if date_start:
            msg = "du " + time.strftime(
                '%d-%m-%Y', time.strptime(date_start, '%Y-%m-%d'))
        else:
            msg = "du début"
        if date_stop:
            msg = msg + " au " + time.strftime(
                '%d-%m-%Y', time.strptime(date_stop, '%Y-%m-%d'))
        else:
            msg = msg + " au " + datetime.now().strftime('%d-%m-%Y')
        return msg

    def _pourcentage(self, num, den):
        if den == 0 or den == "" or den is None:
            return ""
        else:
            return "{0:.1f}%".format(float(num) / den * 100)

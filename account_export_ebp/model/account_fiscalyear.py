# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

from osv import fields, osv


class account_fiscalyear(osv.osv):
    _inherit = "account.fiscalyear"
    _columns = {
        # make the company id mandatory
        'company_id': fields.many2one(
            'res.company', 'Company', required=True,
            help="The company this fiscal year belongs to."),
        'ebp_nb': fields.integer(
            'EBP Fiscal Year Number',
            help="""This value should reflect the number of the fiscal year"""
            """ as used by the EBP accounting software. This should be set"""
            """ to the number of fiscal years recorded in EBP accounting"""
            """ before this one - So for the first year the number is 0,"""
            """ for the second year the number is 1 and so on. This is used"""
            """ for exporting accounting moves to EBP."""),
    }
    _defaults = {
        'ebp_nb': lambda * a: 0
    }

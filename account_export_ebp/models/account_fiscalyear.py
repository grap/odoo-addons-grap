# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountFiscalyear(models.Model):
    _inherit = "account.fiscalyear"

    # TODO Set default, by computing the last number + 1
    ebp_nb = fields.Integer(
        string='EBP Fiscal Year Number', default=0,
        help="This value should reflect the number of the fiscal year"
        " as used by the EBP accounting software. This should be set"
        " to the number of fiscal years recorded in EBP accounting"
        " before this one - So for the first year the number is 0,"
        " for the second year the number is 1 and so on. This is used"
        " for exporting accounting moves to EBP.")

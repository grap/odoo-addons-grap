# -*- coding: utf-8 -*-
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    name = fields.Char(translate=False)

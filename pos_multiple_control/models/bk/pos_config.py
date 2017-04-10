# -*- coding: utf-8 -*-
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # overwrite function to disable constraint on journal control
    @api.multi
    def _check_cash_control(self):
        return True

    _constraints = [
        (
            _check_cash_control,
            "You cannot have two cash controls in one Point Of Sale !",
            ['journal_ids']),
    ]

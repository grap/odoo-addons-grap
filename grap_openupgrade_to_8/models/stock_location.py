# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.model
    def recompute_parent_store(self):
        self._parent_store_compute()
        return True

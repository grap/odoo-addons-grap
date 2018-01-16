# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'
    _order = 'date desc, name'

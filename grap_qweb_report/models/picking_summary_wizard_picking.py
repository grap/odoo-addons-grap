# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class PickingSummaryWizardPicking(models.TransientModel):
    _name = 'picking.summary.wizard.picking'

    wizard_id = fields.Many2one(comodel_name='picking.summary.wizard')

    picking_id = fields.Many2one(comodel_name='stock.picking')

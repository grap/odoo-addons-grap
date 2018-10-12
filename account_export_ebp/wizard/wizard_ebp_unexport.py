# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class WizardEbpUnexport(models.TransientModel):
    _name = 'wizard.ebp.unexport'

    @api.multi
    def button_unexport(self):
        AccountMove = self.env['account.move']
        moves = AccountMove.browse(self.env.context.get('active_ids', False))
        moves.write({'ebp_export_id': False})

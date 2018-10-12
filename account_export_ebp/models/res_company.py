# coding: utf-8
# Copyright (C) 2010 - 2015: Numérigraphe SARL
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # Column Section
    ebp_trigram = fields.Char(
        string='EBP Trigram', compute='_compute_ebp_trigram', store=True)

    @api.multi
    @api.depends('fiscal_type')
    def _compute_ebp_trigram(self):
        for company in self.filtered(
                lambda x: x.fiscal_type in ['fiscal_child', 'fiscal_mother']):
            company.ebp_trigram = company.code

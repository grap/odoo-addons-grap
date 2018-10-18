# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.invoice = self.env.ref('account.invoice_1')
        self.move = self.invoice.move_id

    def test_01_rename_move(self):
        # Allow cancelling entries
        self.move.journal_id.update_posted = True

        # Get sequence
        sequence = self.move.journal_id.sequence_id

        next_name = ("%s%s") % (
            self.move.name[:-sequence.padding],
            str(sequence.number_next_actual).zfill(sequence.padding))

        self.move.rename_account_move_change_number()

        self.assertEqual(
            self.move.name, next_name,
            "Rename of accounting entry failed.")

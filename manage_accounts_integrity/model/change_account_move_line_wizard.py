# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Manage accounts integrity Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

from openerp.osv import fields
from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class change_account_move_line_wizard(TransientModel):
    _name = 'change.account.move.line.wizard'
    _description = 'Wizard to manage move of move lines'

    def default_get(self, cr, uid, pFields, context):
        res = super(change_account_move_line_wizard, self).default_get(
            cr, uid, pFields, context=context)
        account = self.pool.get('account.account').browse(
            cr, uid, context['active_id'], context=context)
        # Get move line without partners per company
        partners = []
        sql_req = """
                SELECT company_id, count(*) as quantity
                FROM account_move_line
                WHERE partner_id is NULL
                AND account_id = %s
                group by company_id
                """ % (account.id)
        cr.execute(sql_req)
        for item in cr.fetchall():
            partners.append((0, 0, {
                'company_id': item[0],
                'move_number': item[1],
                'partner_id': False,
            }))

        res.update({
            'source_account_id': account.id,
            'source_company_id': account.company_id.id,
            'source_type': account.type,
            'source_move_number': account.move_number,
            'source_reconciled_move_number': account.reconciled_move_number,
            'source_closed_period_move_number':
                account.closed_period_move_number,
            'source_invoice_number': account.invoice_number,
            'source_voucher_line_number': account.voucher_line_number,
            'line_ids': partners,
        })
        return res

    # --- Columns
    _columns = {
        'source_account_id': fields.many2one(
            'account.account', 'Source account',
            domain=[('type', '=', 'view')], readonly=True),
        'source_company_id': fields.many2one(
            'res.company', 'Company of the source account', readonly=True),
        'source_type': fields.char(
            'Type of the source account', readonly=True),
        'source_move_number': fields.integer(
            'Number of moves in the source account', readonly=True),
        'source_invoice_number': fields.integer(
            'Number of invoices in the source account', readonly=True),
        'source_voucher_line_number': fields.integer(
            'Number of voucher line in the source account', readonly=True),
        'source_reconciled_move_number': fields.integer(
            'Number of reconciled moves in the source account', readonly=True),
        'source_closed_period_move_number': fields.integer(
            'Number of moves in closed periods', readonly=True),
        'destination_account_id': fields.many2one(
            'account.account', 'Destination account', required=True,
            domain=[('type', '!=', 'view')]),
        'destination_company_id': fields.many2one(
            'res.company', 'Company of the destination account',
            readonly=True),
        'destination_type': fields.char(
            'Type of the destination account', readonly=True),
        'destination_move_number': fields.integer(
            'Number of moves in the destination account', readonly=True),
        'change_view_type': fields.boolean(
            'Change source account in view type'),
        'line_ids': fields.one2many(
            'change.account.move.line.wizard.line', 'wizard_id',
            'Partners list'),
    }

    def onchange_destination_account_id(
            self, cr, uid, ids, destination_account_id, destination_company_id,
            destination_type, destination_move_number, context):
        if destination_account_id:
            account = self.pool.get('account.account').browse(
                cr, uid, destination_account_id, context=context)
            return {'value': {
                'destination_company_id': account.company_id.id,
                'destination_type': account.type,
                'destination_move_number': account.move_number,
            }}
        else:
            return {'value': {
                'destination_company_id': None,
                'destination_type': None,
                'destination_move_number': None,
            }}
        return {}

    def button_change_move_line(self, cr, uid, ids, context=None):
        aa_obj = self.pool.get('account.account')
        ai_obj = self.pool.get('account.invoice')
        am_obj = self.pool.get('account.move')
        aml_obj = self.pool.get('account.move.line')
        ap_obj = self.pool.get('account.period')
        avl_obj = self.pool.get('account.voucher.line')
        reconcile_infos = {}
        close_period_infos = []
        for data in self.browse(cr, uid, ids, context=context):
            # check constraint
            if not (data.source_account_id.company_id.id
                    != data.destination_account_id.company_id.id):
                assert 'Incorrect request', _(
                    """Source and destination account must be belong to the"""
                    """ same company.""")

            # Select all account_move_line to change
            aml_ids = aml_obj.search(cr, uid, [
                ('account_id', '=', data.source_account_id.id),
            ], context=context)

            # Select all account_invoice to change
            ai_ids = ai_obj.search(cr, uid, [
                ('account_id', '=', data.source_account_id.id),
            ], context=context)

            # Select all account_invoice to change
            avl_ids = avl_obj.search(cr, uid, [
                ('account_id', '=', data.source_account_id.id),
            ], context=context)

            if aml_ids:
                # Search reconciled move lines
                aml_reconcile_ids = aml_obj.search(cr, uid, [
                    ('account_id', '=', data.source_account_id.id),
                    ('reconcile_id', '!=', False),
                ], context=context)

                # Select all account_move associated to set them in draft state
                cr.execute("""
                    SELECT distinct(move_id)
                    FROM account_move_line
                    WHERE id in (%s)""" % (str(aml_ids).strip('[]'),))
                move_ids = [r[0] for r in cr.fetchall()]

                # backup reconcile information
                for aml in aml_obj.browse(
                        cr, uid, aml_reconcile_ids, context=context):
                    reconcile_infos[aml.id] = aml.reconcile_id.id

                # Redo reconcile
                aml_obj.write(cr, uid, aml_reconcile_ids, {
                    'reconcile_id': False}, context=context)

                # Backup periods
                cr.execute("""
                    SELECT distinct(period_id)
                    FROM account_move_line aml
                    INNER JOIN account_period ap ON aml.period_id =ap.id
                    WHERE aml.id in (%s)
                    AND ap.state in ('done')
                    """ % (str(aml_ids).strip('[]'),))
                close_period_infos = [r[0] for r in cr.fetchall()]

                # Open Closed periods
                if close_period_infos:
                    ap_obj.action_draft(cr, uid, close_period_infos)

                # Cancel all account_move associated
                am_obj.button_cancel(cr, uid, move_ids, context=context)

                # Change account_move_line account
                aml_obj.write(cr, uid, aml_ids, {
                    'account_id': data.destination_account_id.id
                }, context=context)

                # Change account_move_line partner, if it not set
                for line_id in data.line_ids:
                    aml_partner_ids = aml_obj.search(cr, uid, [
                        ('id', 'in', aml_ids),
                        ('partner_id', '=', False),
                        ('company_id', '=', line_id.company_id.id),
                    ], context=context)
                    aml_obj.write(cr, uid, aml_partner_ids, {
                        'partner_id': line_id.partner_id.id
                    }, context=context)

                # Validate again all account_move associated
                am_obj.button_validate(cr, uid, move_ids, context=context)

                # Redo reconcile
                for aml_reconcile_id in aml_reconcile_ids:
                    aml_obj.write(cr, uid, aml_reconcile_id, {
                        'reconcile_id': reconcile_infos[aml_reconcile_id]
                    }, context=context)

                # Close periods
                # NOTA : A function doesn't exist to do that.
                # (except in a transient model)
                if close_period_infos:
                    mode = 'done'
                    cr.execute("""
                        UPDATE account_journal_period
                        SET state=%s
                        WHERE period_id IN %s""", (
                        mode, tuple(close_period_infos)))
                    cr.execute("""
                        UPDATE account_period
                        SET state=%s
                        WHERE id IN %s""", (
                        mode, tuple(close_period_infos),))

            if ai_ids:
                # change account_invoice account
                ai_obj.write(cr, uid, ai_ids, {
                    'account_id': data.destination_account_id.id
                }, context=context)

            if avl_ids:
                # change account_voucher_line account
                avl_obj.write(cr, uid, avl_ids, {
                    'account_id': data.destination_account_id.id
                }, context=context)

            # (Optional) change type of the source account
            if data.change_view_type:
                aa_obj.write(cr, uid, [data.source_account_id.id], {
                    'type': 'view'}, context=context)
        return {}


class change_account_move_line_wizard_line(TransientModel):
    _name = 'change.account.move.line.wizard.line'
    _description = 'Line of wizard to manage move of move lines'
    _columns = {
        'wizard_id': fields.many2one(
            'change.account.move.line.wizard', 'Wizard Reference',
            select=True),
        'company_id': fields.many2one(
            'res.company', 'Company'),
        'move_number': fields.integer(
            'Number of moves linked to the company', readonly=True),
        'partner_id': fields.many2one(
            'res.partner', 'Partners'),
    }

# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

import base64
import cStringIO
import codecs
from unidecode import unidecode

try:
    import smbc
except:
    smbc = False

from tools.translate import _
from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)

# TODO
# We should write to a temporary file instead, for security and reliability.
# We should raise a clean exception if something goes wrong.


class account_export_ebp(osv.TransientModel):
    _name = "account.export.ebp"

    # Columns Section
    _columns = {
        'name_moves': fields.char('File Name', readonly=True),
        'name_accounts': fields.char('File Name', readonly=True),
        'name_balance': fields.char('File Name', readonly=True),
        'fiscalyear_id': fields.many2one(
            'account.fiscalyear', 'Fiscal year',
            required=True,
            help='Only the moves in this fiscal will be exported'),
        'company_suffix': fields.boolean(
            'Append company\'s code to accounts',
            help="""When this is checked, the company's code will be"""
            """ appended to the receivable and payable accounts' numbers in"""
            """ the exported files on every move line."""),
        'partner_accounts': fields.boolean(
            'Append partners\' code to accounts',
            help="""When this is checked, the partner's special code will"""
            """ be appended to the receivable and payable accounts' numbers"""
            """ in the exported files on every move line where a partner has"""
            """ been specified."""),
        'tax_code_suffix': fields.boolean(
            'Export according to Tax Codes',
            help="""Append Tax Code's suffix to account if the option is"""
            """ checked in the account"""),
        'ignore_draft': fields.boolean(
            'Ignore draft moves',
            help="""Please be aware that draft moves do not not have a"""
            """ move number attached to them. As a consequence, they might"""
            """ not be imported correctly into EBP accounting software"""),
        'ignore_exported': fields.boolean(
            'Ignore moves already exported',
            help="Check this box unless you want to re-export moves to EBP"),
        'download_file': fields.boolean(
            'Download file', help="""Check this box if you want to"""
            """ download the result as a file on your computer. Otherwise,"""
            """ the file will be saved at the place defined in the company"""
            """ settings."""),
        'data_moves': fields.binary('File', readonly=True),
        'data_accounts': fields.binary('File', readonly=True),
        'data_balance': fields.binary('File', readonly=True),
        'exported_moves': fields.integer(
            'Number of moves exported', readonly=True),
        'ignored_moves': fields.integer(
            'Number of moves ignored', readonly=True),
        'exported_lines': fields.integer(
            'Number of lines exported', readonly=True),
        'exported_accounts': fields.integer(
            'Number of accounts exported', readonly=True),
        'state': fields.selection([
            ('export_ebp', 'Prepare Export'),
            ('export_ebp_end', 'Export Done'),
            ('export_ebp_download', 'Ready to download')
        ]),
        'empty_suffixes_partner': fields.boolean(
            'Empty Suffixes Partners', readonly=True),
        'empty_suffixes_tax': fields.boolean(
            'Empty Suffixes Taxes', readonly=True),
    }

    # Defaults Section
    def _get_empty_suffixes_partner(self, cr, uid, context=None):
        rp_obj = self.pool.get('res.partner')
        aml_obj = self.pool.get('account.move.line')

        rp_ids = rp_obj.search(
            cr, uid, [('ref_nb', '=', False)], context=context)
        aml_ids = aml_obj.search(cr, uid, [
            ('date', '>=', '01/12/2012'), ('partner_id', 'in', rp_ids)],
            context=context)

        if aml_ids:
            return True
        return False

    def _get_empty_suffixes_tax(self, cr, uid, context=None):
        atc_obj = self.pool.get('account.tax.code')
        aml_obj = self.pool.get('account.move.line')

        atc_ids = atc_obj.search(
            cr, uid, [('ref_nb', '=', False)], context=context)
        aml_ids = aml_obj.search(cr, uid, [
            ('date', '>=', '01/12/2012'), ('tax_code_id', 'in', atc_ids)],
            context=context)

        if aml_ids:
            return True
        return False

    _defaults = {
        'ignore_exported': lambda * a: True,
        'ignore_draft': lambda * a: True,
        'company_suffix': lambda * a: True,
        'partner_accounts': lambda * a: True,
        'download_file': lambda * a: True,
        'tax_code_suffix': lambda * a: True,
        'state': 'export_ebp',
        'empty_suffixes_partner': _get_empty_suffixes_partner,
        'empty_suffixes_tax': _get_empty_suffixes_tax,
    }

    def export(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        this = self.browse(cr, uid, ids, context=context)[0]
        if this.download_file:
            return self._download(cr, uid, ids, context=context)
        else:
            return self._save(cr, uid, ids, context=context)

    def _download(self, cr, uid, ids, context=None):
        export_obj = self.pool.get('ebp.export')
        if context is None:
            context = {}
        this = self.browse(cr, uid, ids)[0]
        moves_file = cStringIO.StringIO()
        account_file = cStringIO.StringIO()
        balance_file = cStringIO.StringIO()
        export_id = self._export(
            cr, uid, ids, moves_file, account_file, balance_file,
            context=context)
        this.name_moves = "ECRITURES.csv"
        this.name_accounts = "COMPTES.csv"
        this.name_balance = "BALANCES.csv"
        out_moves = base64.encodestring(moves_file.getvalue())
        out_accounts = base64.encodestring(account_file.getvalue())
        out_balance = base64.encodestring(balance_file.getvalue())
        moves_file.close()
        account_file.close()
        balance_file.close()
        self.write(cr, uid, ids, {
            'state': 'export_ebp_download',
            'data_moves': out_moves,
            'data_accounts': out_accounts,
            'data_balance': out_balance,
            'name_moves': this.name_moves,
            'name_accounts': this.name_accounts,
            'name_balance': this.name_balance,
        }, context=context)
        export_obj.write(cr, uid, export_id, {
            'data_accounts': out_accounts,
            'data_balance': out_balance,
            'data_moves': out_moves,
        }, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.export.ebp',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _save(self, cr, uid, ids, context):
        if context is None:
            context = {}

        # Stream writer to convert Unicode to Windows Latin-1
        win_writer = codecs.getwriter('cp1252')

        # Connect to the network share
        company = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).company_id
        data = {'form': self.read(cr, uid, ids, context=context)[0]}
        fiscalyear = self.pool.get('account.fiscalyear').browse(
            cr, uid, data['form']['fiscalyear_id'][0], context)

        path = '%s/Compta.%s' % (company.ebp_uri, fiscalyear.ebp_nb)
        _logger.debug("Connecting to %s as user %s, domain %s" % (
            path, fiscalyear.company_id.ebp_username,
            fiscalyear.company_id.ebp_domain))
        win_share = smbc.Context(
            auth_fn=lambda server, share, workgroup, username, password:
                (fiscalyear.company_id.ebp_domain,
                 fiscalyear.company_id.ebp_username,
                 fiscalyear.company_id.ebp_password))
        moves_file = win_writer(win_share.creat('%s/ECRITURES.TXT' % path))
        account_file = win_writer(win_share.creat('%s/COMPTES.TXT' % path))
        balance_file = win_writer(win_share.creat('%s/BALANCES.TXT' % path))
        self._export(
            cr, uid, ids, moves_file, account_file, context=None)

        # Close the move summaries file
        moves_file.close()
        account_file.close()
        balance_file.close()
#        _logger.debug(
#            """%d line(s) representing %d move(s) exported to"""
#            """ ECRITURES.TXT in %s - %d move(s) ignored""" % (
#                l, len(exported_move_ids), path, len(ignored_move_ids)))

    def _export(
            self, cr, uid, ids, moves_file, account_file, balance_file,
            context=None):
        """
        Export moves files usable by accounting software by EBP version
        3 and above.

        2 files will be produced :
          - a file of accounting moves (ECRITURES.TXT)
          - a file of accounts  (COMPTES.TXT)
        If stored in the right folder, these files will automatically be
        imported next time you open the folder in EBP.

        Lines with an amount of 0 are not ignored even though EBP complains
        about them. This is to raise the attention of the person importing
        them into EBP. Also, journals with a code which does not meet EBP's
        requirements are not ignored.

        Returns a dictionary containing the number of moves and lines
        exported and the number of moves ignored.
        """

        def normalize(text):
            # Remove tricky characters from the string
            if "\n;" in text:
                text = text.replace("\n;", " ")
            if ";" in text:
                text = text.replace(";", " ")
            if "," in text:
                text = text.replace(",", " ")
            if "\"" in text:
                text = text.replace("\"", " ")
            return text

        if context is None:
            context = {}
        export_obj = self.pool.get('ebp.export')

        data = {'form': self.read(cr, uid, ids, context=context)[0]}
        _logger.debug("Form data: %s" % data['form'])

        # Read the EBP year number name from the selected fiscal year
        fiscalyear = self.pool.get('account.fiscalyear').browse(
            cr, uid, data['form']['fiscalyear_id'][0], context)
        user_company = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).company_id

        # Sanity checks
        if context.get('active_model', '') != 'account.move':
            raise osv.except_osv(
                _('Wrong Object'),
                _("This wizard should only be used on accounting moves"))

        # dictionary to store accounts while we loop through move lines
        accounts_data = {}
        # Line counter
        l = 0
        moves = self.pool.get('account.move').browse(
            cr, uid, context.get('active_ids', []), context=context)
        # The move summaries will be written to a CSV file encoded in
        # win-latin-1
        # TODO we should report errors more cleanly to the users here

        tax_code_suffix = data['form']['tax_code_suffix']
        exported_move_ids = []
        ignored_move_ids = []

        # Move File header
        move_line = ','.join([
            "Ligne",
            "Date",
            "Code journal",
            "N° de compte",
            "Intitulé",
            "Pièce",
            "Montant (associé au sens)",
            "Sens",
            "Échéance",
            "Monnaie",
            "Poste analytique"
        ])
        moves_file.write(move_line)
        moves_file.write('\r\n')

        for move in moves:
            # Ignore draft moves unless the user asked for them
            ignore_draft = (
                data['form']['ignore_draft'] and move.state == 'draft')
            # Ignore moves in other fiscal years
            ignore_year = (move.period_id.fiscalyear_id.id !=
                           data['form']['fiscalyear_id'][0])
            # Ignore moves already exported
            ignore_exported = (
                data['form']['ignore_exported'] and move.exported_ebp_id)
            # Skip to next move if this one should be ignored
            if ignore_draft or ignore_year or ignore_exported:
                _logger.debug(
                    """Ignoring move %d - draft: %s, wrong year: %s,"""
                    """ exported: %s""" % (
                        move.id, ignore_draft, ignore_year, ignore_exported))
                ignored_move_ids.append(move.id)
                continue

            _logger.debug("Exporting move %d" % move.id)
            # dictionary to summarize the lines of the move by account
            moves_data = {}
            for line in move.line_id:
                _logger.debug("Examining move line %d" % line.id)

                if line.credit == line.debit:
                    _logger.debug(
                        """Move line %d has a sum equal to zero and will"""
                        """ not be exported.""" % line.id)
                    continue
                # Make up the account number
                account_nb = normalize(line.account_id.code)
                if (data['form']['company_suffix'] and line.company_id and
                    line.company_id.code and (
                        line.account_id.type in ('payable', 'receivable'))):
                    account_nb = account_nb + line.company_id.code
                if (data['form']['partner_accounts'] and line.partner_id and
                    line.partner_id.ref_nb and (
                        line.account_id.type in ('payable', 'receivable'))):
                    # Partner account
                    account_nb = account_nb + line.partner_id.ref_nb
                if (tax_code_suffix and line.account_id.export_tax_code and
                        line.tax_code_id.ref_nb):
                    tmp = account_nb + line.tax_code_id.ref_nb
                    account_nb = tmp

                # Check the most important fields are not above the maximum
                # length so as not to export wrong data with catastrophic
                # consequence
                if len(move.journal_id.code) > 4:
                    raise osv.except_osv(_('Journal code too long'), _(
                        """Journal code '%s' is too long to be exported"""
                        """ to EBP.""") % move.journal_id.code)
                # The docs from EBP state that account codes may be up to
                # 15 characters but "EBP Comptabilité" v13 will refuse anything
                # longer than 10 characters
                if len(account_nb) > 10:
                    raise osv.except_osv(_('Account code too long'), _(
                        """Account code '%s' is too long to be exported to"""
                        """ EBP.""") % account_nb)
                if len(move.name) > 15:
                    raise osv.except_osv(_('Move name too long'), _(
                        """Move name '%s' is too long to be exported to"""
                        """ EBP.""") % move.name)

                # Collect data for the file of move lines
                if account_nb not in moves_data.keys():
                    moves_data[account_nb] = {
                        'date': move.date,
                        'journal': move.journal_id.code,
                        'ref': normalize(
                            ((line.company_id.code + ' ')
                                if line.company_id.code else '') +
                            line.name + (
                                (' (' + move.ref + ')')
                                if move.ref else '')),
                        'name': normalize(move.name),
                        'credit': line.credit,
                        'debit': line.debit,
                        'date_maturity': line.date_maturity,
                        'analytic': line.company_id.code
                    }
                else:
                    moves_data[account_nb]['credit'] += line.credit
                    moves_data[account_nb]['debit'] += line.debit
                    # Keep the earliest maturity date
                    if (line.date_maturity <
                            moves_data[account_nb]['date_maturity']):
                        moves_data[account_nb]['date_maturity'] =\
                            line.date_maturity

                # Collect data for the file of accounts
                # We can't just keep the account_id object because the data
                # we want to export may be partner specific
                if account_nb not in accounts_data.keys():
                    if (data['form']['partner_accounts'] and
                            line.partner_id and line.partner_id.ref_nb and
                            line.account_id.type in ('payable', 'receivable')):
                        # Partner account
                        # Get the default address
                        partner = self.pool.get('res.partner').browse(
                            cr, uid, [line.partner_id.id], context)[0]
                        accounts_data[account_nb] = {
                            'name': normalize(partner.name),
                            'partner_name': normalize(partner.name),
                            'address': normalize(
                                (partner.street or '') +
                                (partner.street2 and
                                    (' ' + partner.street2) or '')),
                            'zip': partner.zip or '',
                            'city': normalize(partner.city or ''),
                            'country': normalize(
                                partner.country_id.name or ''),
                            'contact': normalize(partner.email or ''),
                            'phone': partner.phone or partner.mobile or '',
                            'fax': partner.fax or '',
                        }
                    elif (tax_code_suffix and
                            line.account_id.export_tax_code and
                            line.tax_code_id.ref_nb):
                        accounts_data[account_nb] = {
                            'name': (
                                normalize(line.account_id.name) +
                                '(' + normalize(line.tax_code_id.name) + ')'),
                            'partner_name': '',
                            'address': '',
                            'zip': '',
                            'city': '',
                            'country': '',
                            'contact': '',
                            'phone': '',
                            'fax': '',
                        }
                    else:
                        # Normal account
                        accounts_data[account_nb] = {
                            'name': normalize(line.account_id.name),
                            'partner_name': '',
                            'address': '',
                            'zip': '',
                            'city': '',
                            'country': '',
                            'contact': '',
                            'phone': '',
                            'fax': '',
                        }

                accounts_data[account_nb].setdefault('credit', 0)
                accounts_data[account_nb]['credit'] += line.credit
                accounts_data[account_nb].setdefault('debit', 0)
                accounts_data[account_nb]['debit'] += line.debit

            # Write the move summary to the file
            _logger.debug("Writing the move summary to the file")
            for account_nb, line in moves_data.iteritems():
                l += 1
                if line['credit']:
                    move_line = ','.join([
                        # Line number
                        '%d' % l,
                        # Date (ddmmyy)
                        '%s/%s/%s' % (
                            line['date'][8:10], line['date'][5:7],
                            line['date'][2:4]),
                        # Journal
                        line['journal'].replace(',', '')[:4],
                        # Account number
                        # (possibly with the partner code appended to it)
                        account_nb.replace(',', ''),
                        # Manual title
                        '"%s"' % line['ref'][:40],
                        # Accountable receipt number
                        '"%s"' % line['name'][:15],
                        # Amount
                        '%f' % abs(line['credit']),
                        # [C]redit or [D]ebit
                        'C',
                        # Date of maturity (ddmmyy)
                        line['date_maturity'] and '%s%s%s' % (
                            line['date_maturity'][8:10],
                            line['date_maturity'][5:7],
                            line['date_maturity'][2:4]) or '',
                        # Currency
                        fiscalyear.company_id.currency_id.name.replace(
                            ',', ''),
                        line['analytic'],
                    ])
                    moves_file.write(unidecode(move_line))
                    moves_file.write('\r\n')
                if line['debit']:
                    move_line = ','.join([
                        # Line number
                        '%d' % l,
                        # Date (ddmmyy)
                        '%s/%s/%s' % (
                            line['date'][8:10], line['date'][5:7],
                            line['date'][2:4]),
                        # Journal
                        line['journal'].replace(',', '')[:4],
                        # Account number
                        # (possibly with the partner code appended to it)
                        account_nb.replace(',', ''),
                        # Manual title
                        '"%s"' % line['ref'][:40],
                        # Accountable receipt number
                        '"%s"' % line['name'][:15],
                        # Amount
                        '%f' % abs(line['debit']),
                        # [C]redit or [D]ebit
                        'D',
                        # Date of maturity (ddmmyy)
                        line['date_maturity'] and '%s%s%s' % (
                            line['date_maturity'][8:10],
                            line['date_maturity'][5:7],
                            line['date_maturity'][2:4]) or '',
                        # Currency
                        fiscalyear.company_id.currency_id.name.replace(
                            ',', ''),
                        line['analytic'],
                    ])
                    moves_file.write(unidecode(move_line))
                    moves_file.write('\r\n')
            exported_move_ids.append(move.id)

        # Mark the moves as exported to EBP
        export_id = False
        if len(exported_move_ids):
            export_id = export_obj.create(cr, uid, {
                'fiscalyear_id': fiscalyear.id,
                'company_id': user_company.id,
            }, context=context)
            self.pool.get('account.move').write(cr, uid, exported_move_ids, {
                'exported_ebp_id': export_id,
            }, context=context)

        # Header for Balance File
        line2 = ','.join([
            "Account number",
            "Account name",
            "Debit",
            "Credit",
            "Debit Balance",
            "Credit Balance",
        ])
        balance_file.write(unidecode(line2))
        balance_file.write('\r\n')

        # Write the accounts into the file
        # Write the balance of accounts into the file
        for account_nb, account in accounts_data.iteritems():
            line = ','.join([
                account_nb.replace(',', ''),
                (account['name'] or '').replace(',', '')[:60],
                (account['partner_name'] or '').replace(',', '')[:30],
                (account['address'] or '').replace(',', '')[:100],
                (account['zip'] or '').replace(',', '')[:5],
                (account['city'] or '').replace(',', '')[:30],
                (account['country'] or '').replace(',', '')[:35],
                (account['contact'] or '').replace(',', '')[:35],
                (account['phone'] or '').replace(',', '')[:20],
                (account['fax'] or '').replace(',', '')[:20],
            ])
            account_file.write(unidecode(line))
            account_file.write('\r\n')

            credit = (account['credit'] or 0)
            debit = (account['debit'] or 0)
            if credit > debit:
                credit_balance = credit - debit
                debit_balance = 0
            else:
                credit_balance = 0
                debit_balance = debit - credit

            line2 = ','.join([
                account_nb.replace(',', ''),
                (account['name'] or '').replace(',', '')[:60],
                str(debit),
                str(credit),
                str(debit_balance),
                str(credit_balance),
            ])
            balance_file.write(unidecode(line2))
            balance_file.write('\r\n')

        _logger.debug(
            "%d accounts(s) exported to COMPTES.TXT" % len(accounts_data))

        self.write(cr, uid, ids, {
            'exported_moves': len(exported_move_ids),
            'ignored_moves': len(ignored_move_ids),
            'exported_lines': l,
            'exported_accounts': len(accounts_data),
        }, context=context)
        if export_id:
            export_obj.write(cr, uid, export_id, {
                'exported_moves': len(exported_move_ids),
                'ignored_moves': len(ignored_move_ids),
                'exported_lines': l,
                'exported_accounts': len(accounts_data),
            }, context=context)
        return export_id

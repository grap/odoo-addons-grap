# -*- encoding: utf-8 -*-
################################################################################
#    See __openerp__.py file for Copyright and Licence Informations.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _
from openerp import netsvc

class pos_session(Model):
    _inherit = 'pos.session'

    ### Overload section

    def _confirm_orders(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        period_obj = self.pool.get('account.period')
        order_obj = self.pool.get('pos.order')
        journal_obj = self.pool.get('account.journal')
        move_obj = self.pool.get('account.move')

        for session in self.browse(cr, uid, ids, context=context):
            #parse the lines to group the ids according to the key fields
            groups = {}
            for order in session.order_ids:
                if order.state not in ('paid', 'invoiced'):
                    raise osv.except_osv(
                        _('Error!'),
                        _("You cannot confirm all orders of this session, because they have not the 'paid' status"))
                if order.state == 'paid':
                    keys = (
                        order.partner_id.id,
                        order.date_order[:10])
                    groups.setdefault(keys,[])
                    groups[keys].append(order.id)

            for key in groups.keys():
                (partner_id, date) = key
                order_ids = groups[key]
                journal_id = session.config_id.journal_id.id
                move_vals = {
                    'ref' : session.name, 
                    'journal_id' : journal_id, 
                    'date': date,
                    }

        #        if the journal is set to check the date is in the period, find the period corresponding to the date
                if journal_obj.browse(cr, uid, journal_id, context=context).allow_date:
                    period_id = period_obj.find(cr, uid, dt=date, context=context)[0]
                    move_vals['period_id'] = period_id

                move_id = move_obj.create(cr, uid, move_vals, context=context)
                order_obj._create_account_move_line(cr, uid, order_ids, session, move_id, context=context)
                for order_id in order_ids:
                    wf_service.trg_validate(uid, 'pos.order', order_id, 'done', cr)

        return True


    def wkf_action_close(self, cr, uid, ids, context=None):
        bsl = self.pool.get('account.bank.statement.line')
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if st.difference and st.journal_id.cash_control == True:
                    if st.difference > 0.0:
                        name= _('Point of Sale Profit')
                        account_id = st.journal_id.profit_account_id.id
                    else:
                        account_id = st.journal_id.loss_account_id.id
                        name= _('Point of Sale Loss')
                    if not account_id:
                        raise osv.except_osv( _('Error!'),
                        _("Please set your profit and loss accounts on your payment method '%s'. This will allow OpenERP to post the difference of %.2f in your ending balance. To close this session, you can update the 'Closing Cash Control' to avoid any difference.") % (st.journal_id.name,st.difference))
                    bsl.create(cr, uid, {
                        'statement_id': st.id,
                        'amount': st.difference, 
                        'ref': record.name,
                        'name': name,
                        'account_id': account_id
                    }, context=context)

                if st.journal_id.type == 'bank':
                    st.write({'balance_end_real' : st.balance_end})
                if st.journal_id.type != 'sale':
                    self.button_confirm_pos(cr, uid, [st.id], record.name, context=context)
        return super(pos_session, self).wkf_action_close(cr, uid, ids, context=context)


    ### Private section

    def button_confirm_pos(self, cr, uid, ids, session_name, context=None):
#        this will generate one account_move per bank_statement
        obj_seq = self.pool.get('ir.sequence')
        obj_st = self.pool.get('account.bank.statement')
        if context is None:
            context = {}

        for st in obj_st.browse(cr, uid, ids, context=context):
            j_type = st.journal_id.type
            company_currency_id = st.journal_id.company_id.currency_id.id

            #Preliminary checks
            if not obj_st.check_status_condition(cr, uid, st.state, journal_type=j_type):
                continue

            obj_st.balance_check(cr, uid, st.id, journal_type=j_type, context=context)
            if (not st.journal_id.default_credit_account_id) \
                    or (not st.journal_id.default_debit_account_id):
                raise osv.except_osv(_('Configuration Error!'),
                        _('Please verify that an account is defined in the journal.'))

            if not st.name == '/':
                st_number = st.name
            else:
                c = {'fiscalyear_id': st.period_id.fiscalyear_id.id}
                if st.journal_id.sequence_id:
                    st_number = obj_seq.next_by_id(cr, uid, st.journal_id.sequence_id.id, context=c)
                else:
                    st_number = obj_seq.next_by_code(cr, uid, 'account.bank.statement', context=c)

            for line in st.move_line_ids:
                if line.state <> 'valid':
                    raise osv.except_osv(_('Error!'),
                            _('The account entries lines are not in valid state.'))
            for st_line in st.line_ids:
                if st_line.analytic_account_id:
                    if not st.journal_id.analytic_journal_id:
                        raise osv.except_osv(_('No Analytic Journal!'),_("You have to assign an analytic journal on the '%s' journal!") % (st.journal_id.name,))
                if not st_line.amount:
                    continue

            #parse the lines to group the ids according to the key fields
            groups = {}
            for line in st.line_ids:
                keys = (
                    line.account_id.id, 
                    line.partner_id.id,
                    line.journal_id.id, 
                    st.period_id.id, 
                    st_line.date, 
                    st_line.analytic_account_id, 
                    st_line.amount>0)
                groups.setdefault(keys,[])
                groups[keys].append(line.id)

            #for each group, create account_move and account_move_lines
            i = 0
            for key in groups.keys():
                i +=1
                move_number = st_number + "/" + str(i)
                line_ids = groups[key]
                move_id = self.create_move_from_st_lines(cr, uid, line_ids, st, move_number, session_name, key, context)

            obj_st.write(cr, uid, [st.id], {
                    'name': st_number,
                    'balance_end_real': st.balance_end
            }, context=context)
            obj_st.message_post(cr, uid, [st.id], body=_('Statement %s confirmed, journal items were created.') % (st_number,), context=context)
        if context.get('period_id',False): del context['period_id']
        if context.get('journal_id',False): del context['journal_id']
        return obj_st.write(cr, uid, ids, {'state':'confirm'}, context=context)


    def create_move_from_st_lines(self, cr, uid, ids, st, st_number, session_name, key, context=None):
        """Create the account move and lines from the statement lines.

           :param int/long st_id: ID of the account.bank.statement to create the move from.
           :param int/long company_currency_id: ID of the res.currency of the company
           :param char st_number: will be used as the name of the generated account move
           :return: ID of the account.move created
        """

        if context is None:
            context = {}

        (account_id, partner_id, journal_id, period_id, date, analytic_account_id, debit) = key
        account_move_obj = self.pool.get('account.move')
        account_move_line_obj = self.pool.get('account.move.line')

#        if the journal is set to check the date is in the period, find the period corresponding to the date
        if self.pool.get('account.journal').browse(cr, uid, journal_id, context=context).allow_date:
            period_id = self.pool.get('account.period').find(cr, uid, dt=date, context=context)[0]

        move_vals = {
            'journal_id': journal_id,
            'partner_id': partner_id,
            'period_id': period_id,
            'date': date,
            'name': st_number,
            'ref': session_name,
            }
        move_id = account_move_obj.create(cr, uid, move_vals, context=context)
        bank_move_vals = self._prepare_bank_move_lines_pos(cr, uid, st, move_id, ids, st_number, key, context=context)
        move_line_id = account_move_line_obj.create(cr, uid, bank_move_vals, context=context)

        counterpart_move_vals = self._prepare_counterpart_move_lines_pos(cr, uid, st, move_id, ids, st_number, key, context=context)
        account_move_line_obj.create(cr, uid, counterpart_move_vals, context=context)

        # Bank statements will not consider boolean on journal entry_posted
        account_move_obj.post(cr, uid, [move_id], context=context)
        return move_id

    def _prepare_bank_move_lines_pos(self, cr, uid, st, move_id, ids, st_number, key, context=None):
        """Compute the args to build the dict of values to create the bank move line from a
           statement by calling the _prepare_move_line_vals. This method may be
           overridden to implement custom move generation (making sure to call super() to
           establish a clean extension chain).

           :param browse_record st_line: account.bank.statement.line record to
                  create the move from.
           :param int/long move_id: ID of the account.move to link the move line
           :param float amount: amount of the move line
           :param int/long company_currency_id: ID of currency of the concerned company
           :return: dict of value to create() the bank account.move.line
        """
        (account_id, partner_id, journal_id, period_id, date, anl_id, debit) = key
        amount = 0
        for st_line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
            amount += st_line.amount

        debit = ((amount<0) and -amount) or 0.0
        credit =  ((amount>0) and amount) or 0.0

        return {
            'name': st.name,
            'date': st.date,
            'move_id': move_id,
            'account_id': account_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': st.id,
            'journal_id': journal_id,
            'period_id': period_id,
            'analytic_account_id': anl_id,
        }

    def _prepare_counterpart_move_lines_pos(self, cr, uid, st, move_id, ids, st_number, key, context=None):
        """Compute the args to build the dict of values to create the counter part move line from a
           statement by calling the _prepare_move_line_vals. This method may be
           overridden to implement custom move generation (making sure to call super() to
           establish a clean extension chain).

           :param browse_record st_line: account.bank.statement.line record to
                  create the move from.
           :param int/long move_id: ID of the account.move to link the move line
           :param float amount: amount of the move line
           :param int/long account_id: ID of account to use as counter part
           :param int/long company_currency_id: ID of currency of the concerned company
           :return: dict of value to create() the bank account.move.line
        """
        (account_id, partner_id, journal_id, period_id, date, anl_id, debit) = key
        amount = 0
        for st_line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
            amount += st_line.amount

        acc_id = ((amount<=0) and st.journal_id.default_debit_account_id.id) or st.journal_id.default_credit_account_id.id
        debit = ((amount > 0) and amount) or 0.0
        credit =  ((amount < 0) and -amount) or 0.0

        return {
            'name': st.name,
            'date': st.date,
            'move_id': move_id,
            'account_id': acc_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': st.id,
            'journal_id': journal_id,
            'period_id': period_id,
            'analytic_account_id': anl_id,
        }

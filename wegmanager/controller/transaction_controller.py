import os
import csv
import sys
import tempfile
import time
from datetime import datetime
import hashlib

from tkinter import simpledialog

from fints.models import SEPAAccount

from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.controller.accounts_controller import AccountsController
from wegmanager.controller.fints import FinTS
from wegmanager.view.transactions import Transactions
from wegmanager.view.accounts import Accounts
from wegmanager.model.transaction import Transaction as TransactionModel
from wegmanager.model.transaction_audited import TransactionAudited
from wegmanager.model.bank_user import BankUser
from argparse import ngettext

from wegmanager.controller import db_session


class TransactionController(AbstractController):
    def __init__(self, dtb) -> None:
        super().__init__()
        self.view = None
        self.model = TransactionModel()
        self.dtb = dtb

    def bind(self, view: Transactions):
        self.view = view  # notebook
        data = self.getTableData()
        self.view.create_table(data)  # headers, content = data
        self.view.exportButton.configure(command=self.export)
        self.view.getTransactions.configure(command=self.getAccounts)

    def getTableData(self):
        headers, results = self.dtb.getModeledData(TransactionAudited)
        return headers, results

    def refresh(self):
        data = self.getTableData()
        self.view.create_table(data)

    def get_transactions(self, ac):
        id = int(ac[0])
        with self.dtb.get_session() as dtb:
            bank_user = dtb.query(BankUser).get(id)
            finurl = bank_user.bank.finurl
            custom_fints = bank_user.bank.custom_fints
        postings = self.retreive_transactions(bank_user, finurl)
        self.writetodb(bank_user, custom_fints, postings)

    def retreive_transactions(self, bank_user, finurl):

        account = SEPAAccount(
            iban=bank_user.iban, bic=None, accountnumber=None, subaccount=None,
            blz=str(bank_user.blz))
        pin = bank_user.pin
        if not pin:
            pin = simpledialog.askstring("Input", "Input an String", show='*')
        client = FinTS(account.blz, bank_user.username, pin, finurl)

        client.select_account(account.iban)
        # probably the most reliable way to get all transactions in several
        # requests. From today back max days (usually 90 days). Transactions
        # already requested are identified by hash and ignored.
        days = 90
        raw = client.get_transactions(days)
        postings = client.transform_transactions(raw)
        return postings

    def writetodb(self, bank_user, custom_fints, data):
        '''
        Writes retreived bank transactions in original to 'transactions' table.
        Then it writes some keys from originally retreived bank transactions in
        'transactions_audited.
        '''
        c_transactions = 0
        #c_transactions_audited = 0
        for t in data:

            t['hash'] = self.build_hash(t)
            t['date_retreived'] = datetime.now().replace(microsecond=0)
            t['bank_user_id'] = bank_user.id
            to_store = TransactionModel(**t)
            try:
                transaction_id = self.dtb.setData(to_store)
                c_transactions += 1
            except BaseException as err:
                # TODO: mark doublettes to take care of manually later
                print(t['json_original']['date'], str(
                    t['json_original']["applicant_name"] or ''), str(t['json_original']["amount"]))
                print(_(f'Could not save to database: {err=}, {type(err)=}'))
            finally:
                # get id to try to write to transactions audited at least
                try:
                    with db_session() as dtb:
                        result = dtb.query(TransactionModel.id, TransactionModel.hash).filter(
                            TransactionModel.hash == t['hash']).first()
                    transaction = TransactionModel()
                    transaction_id = result.id
                    self.copy_transactions(
                        transaction_id, t, bank_user.iban, custom_fints)
                except BaseException as err:
                    print(
                        _(f'Could not save transactions to mapped table: {err=}, {type(err)=}'))

        message = ngettext('{0} transaction inserted in database',
                           '{0} transactions inserted in database', c_transactions)
        print(message.format(c_transactions))
        self.refresh()
        return True

    def build_hash(self, t):
        try:
            hash_str = t['json_original']['date'] + \
                t['json_original']['amount']
            hash_str += str(t['json_original'].get('transaction_code', ''))
            hash_str += t['json_original']['purpose'] + \
                (t['json_original']["id"] or '')
            hash_str += str(t['json_original']['applicant_bin'] or '') + \
                str(t['json_original']['applicant_iban'] or '')
            hash_str += str(t['json_original']['applicant_name'] or '') + \
                (t['json_original']["additional_purpose"] or '')
            hash_str += str(t['json_original'].get('end_to_end_reference', '') or '')
        except TypeError as err:
            print(err)
            raise
        hashvalue = hashlib.sha256(hash_str.encode('UTF-8')).hexdigest()
        return hashvalue

    def copy_transactions(self, transaction_id, data, iban, custom_fints):
        try:
            # map keys of our app ("custom_fints.key()") with keys of
            # external bank ("custom_fints.value()")
            audited = {}
            audited['transaction_id'] = transaction_id
            for key, value in custom_fints.items():
                # value is a key for the retreived data!
                if value not in data['json_original']:
                    data['json_original'].pop(value, None)
                    continue
                audited[key] = data['json_original'][value]
            audited['date'] = datetime.strptime(
                audited['date'], '%Y-%m-%d').date()
            to_store = TransactionAudited(**audited)
            self.dtb.setData(to_store)
        except:
            raise

    def export(self):
        headers, content = self.getTableData()

        data = content

        fd, path = tempfile.mkstemp('.csv', 'bank_transactions_')

        with open(path, 'w', newline='', encoding='utf-8') as f:
            # with tempfile.TemporaryFile() as f:
            writer = csv.writer(f)
            try:
                count = 0
                for row in data:
                    if count == 0:

                        # Writing headers of CSV file
                        header = row.keys()
                        writer.writerow(header)
                        count += 1

                    # Writing data of CSV file
                    writer.writerow(row.values())
                f.seek(0)
            except csv.Error as e:
                sys.exit(f'file {path}, line {writer.line}: {e}')
        os.close(fd)
        os.system('/usr/bin/xdg-open ' + path)
        time.sleep(3)
        os.unlink(path)

    def getAccounts(self):
        c = AccountsController(self.dtb)
        v = Accounts(self.view)
        c.bind(v, self.get_transactions)

import os
import csv
import sys
import tempfile
import time

from tkinter import simpledialog

from fints.models import SEPAAccount

from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.controller.accounts_controller import AccountsController
from wegmanager.controller.fints import FinTS
from wegmanager.view.Transactions import Transactions
from wegmanager.view.Accounts import Accounts
from wegmanager.model.Transaction import Transaction as TransactionModel
from argparse import ngettext


class TransactionController(AbstractController):
    def __init__(self, db_session) -> None:
        super().__init__()
        self.view = None
        self.model = TransactionModel()
        self.db_session = db_session

    def bind(self, view: Transactions):
        self.view = view  # notebook
        data = self.getTableData()
        self.view.create_table(data)  # headers, content = data
        self.view.exportButton.configure(command=self.export)
        self.view.getTransactions.configure(command=self.getAccounts)

    def getTableData(self):
        headers, results = self.model.getModeledData(self.db_session)
        return headers, results

    def refresh(self):
        data = self.getTableData()
        self.view.create_table(data)

    def get_transactions(self, ac):
        self.writetodb(self.retreive_transactions(ac))

    def retreive_transactions(self, ac):
        # 1 => blz; 2 => username; 3 => pin, 4 => finurl; 5 => iban
        account = SEPAAccount(
            iban=ac[5], bic=None, accountnumber=None, subaccount=None,
            blz=ac[1])
        pin = ac[3]
        if not pin:
            pin = simpledialog.askstring("Input", "Input an String", show='*')
        client = FinTS(account.blz, ac[2], pin, ac[4])

        client.select_account(account.iban)
        # probably the most reliable way to get all transactions in several
        # requests. From today back max days (usually 90 days). Transactions
        # already requested are identified by hash and ignored.
        days = 90
        raw = client.get_transactions(days)
        postings = client.transform_transactions(raw)
        return postings

    def writetodb(self, data):
        counter = 0
        for t in data:
            try:
                transaction_model = TransactionModel()
                to_store = TransactionModel(**t)
                transaction_model.setData(self.db_session, to_store)
                counter += 1
            except BaseException as err:
                # TODO: mark doublettes to take care of manually later
                print(t['date'].isoformat(), str(
                    t["applicant_name"] or ''), str(t["amount"]))
                print(_(f'Could not save to database: {err=}, {type(err)=}'))
        message = ngettext('{0} transaction inserted in database',
                           '{0} transactions inserted in database', counter)
        print(message.format(counter))
        self.refresh()
        return True

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
        c = AccountsController(self.db_session)
        v = Accounts(self.view)
        c.bind(v, self.get_transactions)

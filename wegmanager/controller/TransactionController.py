from wegmanager.controller.AbstractController import AbstractController
from wegmanager.view.Transactions import Transactions
from wegmanager.view.Accounts import Accounts
from wegmanager.model.Transaction import Transaction as TransactionModel
from wegmanager.controller.AccountsController import AccountsController
import os
import csv
import sys
import tempfile
import time


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

    def export(self):
        headers, content = self.getTableData()

        data = content

        home_folder = os.getenv('HOME')
        filename = os.path.join(home_folder, '.config',
                                'wegmanager', 'tmp_bank_transactions.csv')
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
                sys.exit('file {}, line {}: {}'.format(
                    path, writer.line_num, e))
        os.close(fd)
        os.system('/usr/bin/xdg-open ' + path)
        time.sleep(3)
        os.unlink(path)

    def getAccounts(self):
        c = AccountsController(self.db_session)
        v = Accounts(self.view)
        c.bind(v)

    def refresh(self):
        data = self.getTableData()
        self.view.createTableView(data)


    def getTableData(self):
        headers, results = self.model.getModeledData(self.db_session)
        return headers, results

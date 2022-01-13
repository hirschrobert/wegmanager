from .AbstractController import AbstractController
from view.Transactions import Transactions
from view.Accounts import Accounts
from model.Transaction import Transaction as TransactionModel
from controller.AccountsController import AccountsController
import os
import csv
import sys


class TransactionController(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self.view = None
        self.model = TransactionModel()

    def bind(self, view: Transactions):
        self.view = view  # notebook

        data = self.getTableData()
        self.view.create_table(data)  # headers, content = data
        self.view.exportButton.configure(command=self.export)
        self.view.getTransactions.configure(command=self.getAccounts)

    def export(self):
        headers, content = self.getTableData()

        print(content)
        data = content

        filename = 'bank_transactions.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
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
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(
                    filename, writer.line_num, e))
                f.close

        f.close()
        #os.startfile('data_file.csv', 'open')
        os.system('/usr/bin/xdg-open ' + filename)

    def getAccounts(self):
        c = AccountsController()
        v = Accounts(self.view)
        c.bind(v)

    def refresh(self):
        data = self.getTableData()
        self.view.createTableView(data)

    def update(self):
        self.view.createAddView()

    def getTableData(self):
        headers, results = self.model.getModeledData()
        return headers, results

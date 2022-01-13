from controller.FinTS import FinTS
from tkinter import simpledialog, messagebox
from model.BankUser import BankUser
from model.Transaction import Transaction
from fints.models import SEPAAccount


class AccountsController():
    def __init__(self) -> None:

        self.model = BankUser()
        self.entries_values = {}
        self.view = None

    def bind(self, view):
        self.view = view
        data = self.getAccountsData()
        self.view.createTableView(data)  # headers, content = data
        self.view.getPostingsButton.configure(command=self.getTransactions)
        self.view.addAccountButton.configure(command=self.addAccount)
        # self.view.destroyAddView(data)

    def getTransactions(self):
        self.writetodb(self.retreiveTransactions())

    def retreiveTransactions(self):
        ac = self.view.showAccounts()
        # 1 => blz; 2 => username; 3 => pin, 4 => finurl; 5 => iban
        account = SEPAAccount(
            iban=ac[5], bic=None, accountnumber=None, subaccount=None, blz=ac[1])
        pin = ac[3]
        if not pin:
            pin = simpledialog.askstring("Input", "Input an String", show='*')
        client = FinTS(account.blz, ac[2], pin, ac[4])

        client.select_account(account.iban)
        days = 90
        raw = client.get_transactions(days)
        postings = client.transform_transactions(raw)
        #print(json.dumps(postings, indent=4, sort_keys=True, default=str))
        #transactions = json.dumps(postings, indent=4, sort_keys=True, default=str)
        # return transactions
        return postings

    def writetodb(self, data):
        for t in data:
            try:
                transaction_model = Transaction()
                to_store = Transaction(**t)
                transaction_model.setData(to_store)
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
        return True

    def getAccounts(self):
        account = self.view.showAccounts()
        if not account[3]:
            pin = simpledialog.askstring("Input", "Input an String", show='*')
        else:
            pin = account[3]
        client = FinTS(account[1], account[2], pin, account[4])
        accounts = client.getAccounts()
        print(accounts)

    def getAccountsData(self):
        headers, results = self.model.getModeledData()
        return headers, results

    def update(self):
        data = self.getAccountsData()
        self.view.createTableView(data)  # headers, content = data

    def addAccount(self):
        self.view.createAddView()

    def addAccountData(self, inputs):
        if self.validate_entries(inputs):
            data = {
                "iban": self.entries_values["iban"],
                "username": self.entries_values["username"],
                "pin": self.entries_values["pin"],
                "blz": self.entries_values["blz"],
                "finurl": self.entries_values["finurl"]
            }

            to_store = BankUser(**data)
            self.model.setData(to_store)
            return True
        return False

    def validate_entries(self, entries):
        isvalid = True
        for key, item in entries.items():
            # case (blz < 10000000 && > 99999999)
            if key == "blz":
                try:
                    value = int(item.get())
                    if (value < 10000000 or value > 99999999):
                        raise ValueError
                    self.entries_values[key] = value
                except ValueError:
                    isvalid = False
                    self.entries_values[key] = None
                    messagebox.showerror(
                        title="Validation error", message=_(f"{key}: must be eight digits")
                    )
            else:
                value = item.get()
                self.entries_values[key] = value

        return isvalid

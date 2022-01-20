from wegmanager.controller.FinTS import FinTS
from tkinter import simpledialog, messagebox
from wegmanager.model.BankUser import BankUser
from wegmanager.model.Transaction import Transaction
from fints.models import SEPAAccount


class AccountsController():
    def __init__(self, db_session) -> None:
        self.view = None
        self.model = BankUser()
        self.entries_values = {}
        self.db_session = db_session

    def bind(self, view):
        self.view = view
        data = self.getAccountsData(self.db_session)
        self.view.createTableView(data)  # headers, content = data
        self.view.getPostingsButton.configure(command=self.getTransactions)
        self.view.addAccountButton.configure(command=self.w2controller)

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
        # probably the most reliable way to get all transactions in several
        # requests. From today back max days (usually 90 days). Transactions
        # already requested are identified by hash and ignored.
        days = 90
        raw = client.get_transactions(days)
        postings = client.transform_transactions(raw)
        return postings

    def writetodb(self, data):
        for t in data:
            try:
                transaction_model = Transaction()
                to_store = Transaction(**t)
                transaction_model.setData(self.db_session, to_store)
            except BaseException as err:
                # TODO: mark doublettes to take care of manually later
                print(t['date'].isoformat(), str(t["applicant_name"] or ''), str(t["amount"]))
                print(f"Unexpected {err=}, {type(err)=}")
            finally:
                pass
                #update transaction table
        return True

    def getAccountsData(self, db_session):
        headers, results = self.model.getModeledData(db_session)
        return headers, results

    def update(self):
        data = self.getAccountsData(self.db_session)
        self.view.createTableView(data)  # headers, content = data

    # V
    # V controller for adding new bank account form

    def w2controller(self):
        #self.view.add_callback('import', self.addAccountData)
        self.view.createAddView(self.addAccountData)

    def addAccountData(self):
        if self.validate_entries(self.view.inputs):
            data = {
                "iban": self.entries_values["iban"],
                "username": self.entries_values["username"],
                "pin": self.entries_values["pin"],
                "blz": self.entries_values["blz"],
                "finurl": self.entries_values["finurl"]
            }

            to_store = BankUser(**data)
            self.model.setData(self.db_session, to_store)
            self.update()
            self.view.destroyAddView()

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

from tkinter import messagebox
from wegmanager.model.BankUser import BankUser


class AccountsController():
    def __init__(self, db_session) -> None:
        self.view = None
        self.model = BankUser()
        self.entries_values = {}
        self.db_session = db_session

    def bind(self, view, callback):
        self.view = view
        data = self.getAccountsData(self.db_session)
        self.view.createTableView(data)  # headers, content = data
        self.view.getPostingsButton.configure(command=lambda: callback(self.view.showAccounts()))
        self.view.addAccountButton.configure(command=self.w2controller)

    def getAccountsData(self, db_session):
        headers, results = self.model.getModeledData(db_session)
        return headers, results

    def update(self):
        data = self.getAccountsData(self.db_session)
        self.view.createTableView(data)  # headers, content = data

    # V
    # V controller for adding new bank account form

    def w2controller(self):
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
                        title="Validation error",
                        message=_(f"{key}: must be eight digits")
                    )
            else:
                value = item.get()
                self.entries_values[key] = value

        return isvalid

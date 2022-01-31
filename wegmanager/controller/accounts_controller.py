# -*- coding: utf-8 -*-
from tkinter import messagebox
from wegmanager import DEBUG
from wegmanager.model.bank_user import BankUser
from wegmanager.model.bank import Bank
from wegmanager.controller.util import validated_iban


class AccountsController():
    def __init__(self, dtb) -> None:
        self.view = None
        self.model = BankUser()
        self.entries_values = {}
        self.dtb = dtb

    def bind(self, view, callback):
        self.view = view
        data = self.get_accounts_data()
        self.view.createTableView(data)  # headers, content = data
        self.view.getPostingsButton.configure(
            command=lambda: callback(self.view.showAccounts()))
        self.view.addAccountButton.configure(command=self.w2controller)

    def get_accounts_data(self):
        headers, results = self.dtb.getModeledData(self.model)
        return headers, results

    def update(self):
        data = self.get_accounts_data()
        self.view.createTableView(data)  # headers, content = data

    # V
    # V controller for adding new bank account form

    def w2controller(self):
        callbacks = {}
        callbacks['add_account_data'] = self.add_account_data
        callbacks['get_bank_by_id'] = self.get_bank_by_id
        self.view.createAddView(self.get_banks_tuple(),
                                **callbacks)

    def get_banks_tuple(self):
        columns = [Bank.id, Bank.name]
        return self.dtb.get_column_data(*columns)

    def get_bank_by_id(self, bank_id):
        res = self.dtb.get_by_id(bank_id)
        return res

    def add_account_data(self):
        if self.validate_entries(self.view.inputs):
            data = {
                "iban": self.entries_values["iban"],
                "username": self.entries_values["username"],
                "pin": self.entries_values["pin"],
                "blz": self.entries_values["blz"],
                "bank_id": self.entries_values["bank_id"]
            }
            to_store = BankUser(**data)
            self.dtb.setData(to_store)
            self.update()
            self.view.destroyAddView()

    def validate_entries(self, entries):
        if DEBUG:
            return True

        is_valid = True
        messages = {}
        for key, item in entries.items():
            # case (blz < 10000000 && > 99999999)
            if key == "blz":
                tmp = item.get()
                if not tmp:
                    tmp = '0'
                value = int((tmp).replace(" ", ""))
                if (value < 10000000 or value > 99999999):
                    self.entries_values[key] = None
                    is_valid = False
                    messages[key] = _("BLZ: Must be eight digits.")
                else:
                    self.entries_values[key] = value
            # value doesn't come from input and must not be empty.
            elif key == 'bank_id':
                if not item:
                    self.entries_values[key] = None
                    is_valid = False
                    messages[key] = _("Bank: Please select a bank.")
                else:
                    self.entries_values[key] = item
            # get rid of spaces
            elif key == 'iban':
                value = item.get().replace(" ", "")
                # !A AND B <==> B (inhibition)
                if not validated_iban(value, entries['blz'].get()):
                    self.entries_values[key] = None
                    is_valid = False
                    messages[key] = _("IBAN: Not a valid IBAN.")
                self.entries_values[key] = value
                # TODO: Validate IBAN
            else:
                value = item.get()
                self.entries_values[key] = value
        try:
            if not is_valid:
                raise ValueError
        except ValueError:
            message = ""
            for key in messages:
                message += messages[key] + "\n"
            messagebox.showerror(
                title=_("Validation Error"),
                message=message
            )

        return is_valid

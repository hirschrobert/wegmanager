import tkinter as tk
from tkinter import ttk
from typing import List

from wegmanager.controller.fints import AccountNotFoundException
from wegmanager.view.widgets import Combobox


class Accounts:
    def __init__(self, parent=None):
        self.parent = parent  # Transactions view
        self.w1 = tk.Toplevel(self.parent)
        self.w1.title(_('Bank Accounts'))
        self.w1.group(self.parent.parent)
        self.createButtonView()
        self.createPopup()
        self.table = None
        self.w2 = None
        self.inputs = {}
        self.cmb = None

    def createTableView(self, data: List):
        self.create_table(self.w1, data)
        self.table.bind("<Button-3>", self.openPopup)

    def create_table(self, frame, data: List):
        headers, content = data
        if content[0]:
            tableheaders = list(content[0].keys())
        else:
            tableheaders = list(headers.keys())
        self.table = ttk.Treeview(
            frame, show="headings", columns=tableheaders)
        self.table.grid(column=0, row=0, columnspan=2,
                        sticky=tk.W + tk.E + tk.N + tk.S)

        displaycolumns = []
        for col in self.table["columns"]:
            if "%s" % col in headers.keys():
                displaycolumns.append(col)
        self.table["displaycolumns"] = displaycolumns

        for key, value in headers.items():
            self.table.heading(key, text=value)
        if not content[0]:
            self.disablePopup(self.popup)
        else:
            for row in content:
                self.table.insert("", tk.END, values=list(row.values()))

    def createButtonView(self):
        self.getPostingsButton = ttk.Button(self.w1, text=_(
            "request bank posting"))
        self.getPostingsButton.grid(
            column=0, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.addAccountButton = tk.Button(self.w1)
        self.addAccountButton["text"] = _("add bank account")
        self.addAccountButton.grid(
            row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

    def createPopup(self):
        self.popup = tk.Menu(self.w1, tearoff=False)
        self.popup.add_command(label=_("change"))
        self.popup.add_separator()
        self.popup.add_command(label=_("delete"), command=self.delete)

    def disablePopup(self, menu):
        for index in range(menu.index('end') + 1):
            if "state" in menu.entryconfigure(index):
                menu.entryconfigure(index, state="disabled")

    def openPopup(self, e):
        self.popup.tk_popup(e.x_root, e.y_root)

    def selection(self):
        results = []
        for item in self.table.selection():
            values = self.table.item(item, "values")
            results.append(values)
        if len(results) > 0:
            return results[0]
        else:
            raise AccountNotFoundException()

    def change(self):
        items = self.selection()
        for i in items:
            print(i[0] + "changed")

    def delete(self):
        items = self.selection()
        for i in items:
            print(i[0] + "deleted")

    def showAccounts(self):
        account = self.selection()
        return account

    # V
    # V form view for adding new bank account

    def createAddView(self, values, **callbacks):
        self.w2 = tk.Toplevel(self.w1)
        self.w2.title(_('Add Bank Account'))
        self.w2.group(self.parent)

        # iban
        iban_label = ttk.Label(self.w2, text=_("IBAN") + ":")
        iban_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.inputs["iban"] = ttk.Entry(self.w2)
        self.inputs["iban"].grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # username
        username_label = ttk.Label(self.w2, text=_("Username") + ":")
        username_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.inputs["username"] = ttk.Entry(self.w2)
        self.inputs["username"].grid(
            column=1, row=1, sticky=tk.E, padx=5, pady=5)
        
        # customername
        customername_label = ttk.Label(self.w2, text=_("Customer ID") + ":")
        customername_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.inputs["customername"] = ttk.Entry(self.w2)
        self.inputs["customername"].grid(
            column=1, row=2, sticky=tk.E, padx=5, pady=5)

        # pin
        pin_label = ttk.Label(self.w2, text=_("Pin") + ":")
        pin_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        self.inputs["pin"] = ttk.Entry(self.w2, show="*")
        self.inputs["pin"].grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        # blz
        blz_label = ttk.Label(self.w2, text=_("German Bank Code (BLZ)") + ":")
        blz_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        self.inputs["blz"] = ttk.Entry(self.w2)
        self.inputs["blz"].grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        # finurl
        finurl_label = ttk.Label(self.w2, text=_("Select your bank") + ":")
        finurl_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.inputs["bank_id"] = None
        self.cmb = Combobox(frame=self.w2, values=values, row=5,
                            column=1, callback=self.inputs)

        # add account button
        addAccountDataButton = ttk.Button(self.w2, text=_(
            "Add Bank Account"), command=callbacks['add_account_data'])
        addAccountDataButton.grid(
            column=0, row=6, sticky=tk.E, padx=5, pady=5)

        # cancel button
        cancel_button = ttk.Button(self.w2, text=_(
            "Cancel"), command=self.w2.destroy)
        cancel_button.grid(column=1, row=6, sticky=tk.E, padx=5, pady=5)

    def update_input(self):
        self.inputs["bank"] = self.cmb.get()

    def destroyAddView(self):
        self.w2.destroy()

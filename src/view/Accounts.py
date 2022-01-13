import tkinter as tk
from tkinter import ttk
from typing import List
from controller.AccountsController import AccountsController


class Accounts:
    def __init__(self, parent=None):
        self.parent = parent  # Transactions view
        self.w1 = tk.Toplevel(self.parent)
        self.w1.title(_('Bank Accounts'))
        self.w1.group(self.parent.parent)
        self.createButtonView()
        self.createPopup()
        self.controller = AccountsController()
        self.room_types = None
        self.table = None
        self.neighbourhoods = None
        self.w2 = None

    def createTableView(self, data: List):
        self.create_table(self.w1, data)
        self.table.bind("<Button-3>", self.openPopup)

    def create_table(self, frame, data: List):
        headers, content = data
        print(content)
        if content[0]:
            tableheaders = list(content[0].keys())
        self.table = ttk.Treeview(
            frame, show="headings", columns=tableheaders)

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
                #result = [row[key] for key in headers.keys()]
                self.table.insert("", tk.END, values=list(row.values()))

        self.table.grid(row=0, columnspan=2)

    def createButtonView(self):
        self.getPostingsButton = tk.Button(self.w1)
        self.getPostingsButton["text"] = _("request bank posting")
        self.getPostingsButton.grid(
            row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.addAccountButton = tk.Button(self.w1)
        self.addAccountButton["text"] = _("add bank account")
        self.addAccountButton.grid(
            row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

    def createPopup(self):
        self.popup = tk.Menu(self.w1, tearoff=False)
        self.popup.add_command(
            label=_("change"), command=self.createChangeView)
        self.popup.add_separator()
        self.popup.add_command(label=_("delete"), command=self.delete)

    def disablePopup(self, menu):
        for index in range(menu.index('end') + 1):
            if "state" in menu.entryconfigure(index):
                menu.entryconfigure(index, state="disabled")

    def openPopup(self, e):
        self.popup.tk_popup(e.x_root, e.y_root)

    def createAddView(self):
        self.w2 = tk.Toplevel(self.parent)
        self.w2.title(_('Add Bank Account'))
        self.w2.group(self.parent)

        inputs = {}
        # iban
        iban_label = ttk.Label(self.w2, text=_("IBAN") + ":")
        iban_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        inputs["iban"] = ttk.Entry(self.w2)
        inputs["iban"].grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # username
        username_label = ttk.Label(self.w2, text=_("Username") + ":")
        username_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        inputs["username"] = ttk.Entry(self.w2)
        inputs["username"].grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # pin
        pin_label = ttk.Label(self.w2, text=_("Pin") + ":")
        pin_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        inputs["pin"] = ttk.Entry(self.w2, show="*")
        inputs["pin"].grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        # blz
        blz_label = ttk.Label(self.w2, text=_("German Bank Code") + ":")
        blz_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        inputs["blz"] = ttk.Entry(self.w2)
        inputs["blz"].grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        # finurl
        finurl_label = ttk.Label(self.w2, text=_("FinTS Bank URL") + ":")
        finurl_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        inputs["finurl"] = ttk.Entry(self.w2)
        inputs["finurl"].grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        # login button
        addAccountDataButton = ttk.Button(self.w2, text=_(
            "Add Bank Account"), command=lambda: self.destroyAddView(inputs))
        addAccountDataButton.grid(column=0, row=5, sticky=tk.E, padx=5, pady=5)

        # cancel button
        cancel_button = ttk.Button(self.w2, text=_(
            "Cancel"), command=self.w2.destroy)
        cancel_button.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)

    def destroyAddView(self, inputs):
        if self.controller.addAccountData(inputs):
            data = self.controller.getAccountsData()
            self.createTableView(data)
            self.w2.destroy()

    def createChangeView(self):
        w1 = tk.Toplevel(self.parent)
        w1.title(_('Add Invoice'))
        w1.group(self.parent)

        items = self.selection()
        print(items[0])
        self.neighbourhoods = [
            "Entrepôt",
            "Hôtel-de-Ville",
            "Opéra",
            "Ménilmontant",
            "Louvre"
        ]
        self.room_types = [
            "Entire home/apt",
            "Private room",
            "Shared room",
            "Hotel room"
        ]

    def selection(self):
        results = []
        for item in self.table.selection():
            values = self.table.item(item, "values")
            results.append(values)
        return results[0]

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

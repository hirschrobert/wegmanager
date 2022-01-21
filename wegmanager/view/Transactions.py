from tkinter import ttk
import tkinter as tk
from typing import List

from wegmanager.view.AbstractTab import AbstractTab
from wegmanager.view.Form import Form


class Transactions(AbstractTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        # self is Transactions, which is an AbstractTab which is a Frame
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.createButtonView()
        self.createPopup()

    def create_table(self, data: List):
        headers, content = data
        if content[0]:
            tableheaders = list(content[0].keys())
        else:
            tableheaders = list(headers.keys())
        self.table = ttk.Treeview(
            self, show="headings", columns=tableheaders)
        self.table.grid(column=0, row=1, columnspan=4,
                        sticky=tk.W + tk.E + tk.N + tk.S)
        self.table.bind("<Button-3>", self.openPopup)

        hscroll = ttk.Scrollbar(self, orient='horizontal')
        hscroll .configure(command=self.table.xview)
        self.table.configure(xscrollcommand=hscroll .set)
        hscroll.grid(column=0, row=2, columnspan=4, sticky=tk.W + tk.E + tk.S)

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

        bframe = tk.Frame(self)
        bframe.grid(column=0, row=0, sticky=tk.N + tk.W, padx=5, pady=5)

        search_label = ttk.Label(bframe, text=_("Search") + ":")
        search_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        search_input = ttk.Entry(bframe, width=50)
        search_input.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

        self.getTransactions = tk.Button(bframe)
        self.getTransactions["text"] = _("get new bank transactions")
        self.getTransactions.grid(column=3, row=0, sticky=tk.W)

        self.exportButton = tk.Button(bframe)
        self.exportButton["text"] = _("export")
        self.exportButton.grid(column=2, row=0, sticky=tk.W)

    def createAddView(self):
        w1 = tk.Toplevel(self.master)
        w1.title(_('Add Invoice'))
        w1.group(self.master)

    def createChangeView(self):
        w1 = tk.Toplevel(self.master)
        w1.title(_('Add Invoice'))
        w1.group(self.master)
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
            "Entire home/apt" "Private room",
            "Shared room",
            "Hotel room"
        ]
        self.view = Form(w1)
        self.view.create_view(self.neighbourhoods, self.room_types)

    def createPopup(self):
        self.popup = tk.Menu(self.master, tearoff=False)
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

    def selection(self):
        results = []
        for item in self.table.selection():
            values = self.table.item(item, "values")
            results.append(values)
        return results

    def change(self):
        items = self.selection()
        for i in items:
            print(i[0] + "changed")

    def delete(self):
        items = self.selection()
        for i in items:
            print(i[0] + "deleted")

import tkinter as tk
from tkinter import ttk, filedialog as fd
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from locale import atof

from tkcalendar import DateEntry
from os import path

from wegmanager.view.AbstractTab import AbstractTab


class Invoices(AbstractTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="invoice")
        self.grid_columnconfigure(1, weight=1, uniform="booking")
        # self is Invoices, which is an AbstractTab which is a Frame
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.booking_frame = None
        self.invoice_frame = None
        self.callbacks = {}
        self.create_buttons()
        self.cents = Decimal('.01')

    def create_buttons(self):
        self.exportButton = tk.Button(self)
        self.exportButton["text"] = _("export")
        self.exportButton.grid(row=1, column=0, sticky=tk.W)

    def create_invoice_form(self, home_path):
        self.home_path = home_path
        self.invoice_frame = tk.LabelFrame(
            self, text=_("Invoice Fields"))
        self.invoice_frame.grid(
            row=0, column=0, sticky=tk.N + tk.W + tk.S + tk.E, padx=5, pady=5)

        self.invoice_form = {'label': {},
                             'entry': {},
                             'combo': {'taxes': {},
                                       'amount_total': {}},
                             'file': {}
                             }

        self.invoice_form['label']['invoice_date'] = ttk.Label(
            self.invoice_frame, text=_("Invoice Date") + ":")
        self.invoice_form['label']['invoice_date'].grid(
            column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['invoice_date'] = DateEntry(
            self.invoice_frame)
        self.invoice_form['entry']['invoice_date'].configure(validate='none')
        self.invoice_form['entry']['invoice_date'].delete(0, "end")
        self.invoice_form['entry']['invoice_date'].grid(
            column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['date_registered'] = ttk.Label(
            self.invoice_frame, text=_("Date Registered") + ":")
        self.invoice_form['label']['date_registered'].grid(
            column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['date_registered'] = DateEntry(
            self.invoice_frame)
        self.invoice_form['entry']['date_registered'].configure(
            validate='none')
        self.invoice_form['entry']['date_registered'].delete(0, "end")
        self.invoice_form['entry']['date_registered'].grid(
            column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['invoice_number'] = ttk.Label(
            self.invoice_frame, text=_("Invoice Number") + ":")
        self.invoice_form['label']['invoice_number'].grid(
            column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['invoice_number'] = ttk.Entry(
            self.invoice_frame)
        self.invoice_form['entry']['invoice_number'].grid(
            column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['description'] = ttk.Label(
            self.invoice_frame, text=_("Description") + ":")
        self.invoice_form['label']['description'].grid(
            column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['description'] = ttk.Entry(
            self.invoice_frame)
        self.invoice_form['entry']['description'].grid(
            column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['currency'] = ttk.Label(
            self.invoice_frame, text=_("Currency") + ":")
        self.invoice_form['label']['currency'].grid(
            column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['currency'] = ttk.Entry(
            self.invoice_frame)
        self.invoice_form['entry']['currency'].insert(
            tk.END, 'EUR')
        self.invoice_form['entry']['currency'].grid(
            column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['taxes'] = ttk.Label(
            self.invoice_frame, text=_("Amount taxed") + ":")
        self.invoice_form['label']['taxes'].grid(
            column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.invoice_form['combo']['taxes']['frame'] = tk.Frame(
            self.invoice_frame)
        self.invoice_form['combo']['taxes']['frame'].grid(
            column=1, row=5, sticky=tk.E)

        self.all_entries = []
        self.add_more_taxes()

        self.invoice_form['combo']['taxes']['more_button'] = tk.Button(self.invoice_form['combo']['taxes']['frame'],
                                                                       text="+", command=self.add_more_taxes)
        self.invoice_form['combo']['taxes']['more_button'].grid(
            column=0, row=0, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['combo']['taxes']['less_button'] = tk.Button(self.invoice_form['combo']['taxes']['frame'],
                                                                       text="-", command=self.delete_last_taxes)
        self.invoice_form['combo']['taxes']['less_button'].grid(
            column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['amount_total'] = ttk.Label(
            self.invoice_frame, text=_("Total Amount") + ":")
        self.invoice_form['label']['amount_total'].grid(
            column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.invoice_form['combo']['amount_total']['frame'] = tk.Frame(
            self.invoice_frame)
        self.invoice_form['combo']['amount_total']['frame'].grid(
            column=1, row=6, sticky=tk.E)

        # sum of amounts pretax + tax amounts
        self.invoice_form['entry']['amount_total'] = ttk.Label(
            self.invoice_form['combo']['amount_total']['frame'], text="0,00")
        self.invoice_form['entry']['amount_total'].grid(
            column=0, row=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # sum of amounts pretax + tax amounts
        self.invoice_form['combo']['amount_total']['eq'] = ttk.Label(
            self.invoice_form['combo']['amount_total']['frame'], text=" = ")
        self.invoice_form['combo']['amount_total']['eq'].grid(
            column=2, row=0, sticky=tk.W, padx=5, pady=5)

        # sum of amounts pretax
        self.invoice_form['combo']['amount_total']['total_pretax'] = ttk.Label(
            self.invoice_form['combo']['amount_total']['frame'], text="0,00")
        self.invoice_form['combo']['amount_total']['total_pretax'].grid(
            column=3, row=0, sticky=tk.E, padx=5, pady=5)

        # sum of amounts pretax
        self.invoice_form['combo']['amount_total']['pl'] = ttk.Label(
            self.invoice_form['combo']['amount_total']['frame'], text=" + ")
        self.invoice_form['combo']['amount_total']['pl'].grid(
            column=4, row=0, sticky=tk.E, padx=5, pady=5)

        # sum of tax amounts
        self.invoice_form['combo']['amount_total']['total_tax'] = ttk.Label(
            self.invoice_form['combo']['amount_total']['frame'], text="0,00")
        self.invoice_form['combo']['amount_total']['total_tax'].grid(
            column=5, row=0, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['amount_handyman'] = ttk.Label(
            self.invoice_frame, text=_("Amount Handyman") + ":")
        self.invoice_form['label']['amount_handyman'].grid(
            column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['amount_handyman'] = ttk.Entry(
            self.invoice_frame)
        self.invoice_form['entry']['amount_handyman'].grid(
            column=1, row=7, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['amount_material'] = ttk.Label(
            self.invoice_frame, text=_("Amount material") + ":")
        self.invoice_form['label']['amount_material'].grid(
            column=0, row=8, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['amount_material'] = ttk.Entry(
            self.invoice_frame)
        self.invoice_form['entry']['amount_material'].grid(
            column=1, row=8, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['date_service_beginn'] = ttk.Label(
            self.invoice_frame, text=_("Date Service Begin") + ":")
        self.invoice_form['label']['date_service_beginn'].grid(
            column=0, row=9, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['date_service_beginn'] = DateEntry(
            self.invoice_frame)
        self.invoice_form['entry']['date_service_beginn'].configure(
            validate='none')
        self.invoice_form['entry']['date_service_beginn'].delete(0, "end")
        self.invoice_form['entry']['date_service_beginn'].grid(
            column=1, row=9, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['date_service_end'] = ttk.Label(
            self.invoice_frame, text=_("Date Service End") + ":")
        self.invoice_form['label']['date_service_end'].grid(
            column=0, row=10, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['date_service_end'] = DateEntry(
            self.invoice_frame)
        self.invoice_form['entry']['date_service_end'].configure(
            validate='none')
        self.invoice_form['entry']['date_service_end'].delete(0, "end")
        self.invoice_form['entry']['date_service_end'].grid(
            column=1, row=10, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['status'] = ttk.Label(
            self.invoice_frame, text=_("Status") + ":")
        self.invoice_form['label']['status'].grid(
            column=0, row=11, sticky=tk.W, padx=5, pady=5)

        self.invoice_form['entry']['status'] = ttk.Combobox(
            self.invoice_frame, values=["", _("paid"), _("open"),
                                        _("disputed"), _("cancelled")])
        self.invoice_form['entry']['status'].grid(
            column=1, row=11, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['notes'] = ttk.Label(
            self.invoice_frame, text=_("Notes") + ":")
        self.invoice_form['label']['notes'].grid(
            column=0, row=12, sticky=tk.W, padx=5, pady=5)
        self.invoice_form['entry']['notes'] = tk.Text(
            self.invoice_frame, width=30, height=4)
        self.invoice_form['entry']['notes'].grid(
            column=1, row=12, sticky=tk.E, padx=5, pady=5)

        self.invoice_form['label']['file'] = ttk.Label(
            self.invoice_frame, text=_("File") + ":")
        self.invoice_form['label']['file'].grid(
            column=0, row=13, sticky=tk.W, padx=5, pady=5)

        self.invoice_form['file']['frame'] = tk.Frame(self.invoice_frame)
        self.invoice_form['file']['frame'].grid(
            column=1, row=13, sticky=tk.E, padx=5, pady=5)
        open_button = ttk.Button(self.invoice_form['file']['frame'], text=_(
            "Select a File..."), command=self.select_file)
        open_button.grid(
            column=0, row=0, sticky=tk.E, padx=5, pady=5)
        self.invoice_form['entry']['file'] = ''
        self.file_label = tk.Label(
            self.invoice_form['file']['frame'], width=20, text="")
        self.file_label.grid(
            column=0, row=1, sticky=tk.E, padx=5, pady=5)

        add_button = ttk.Button(self.invoice_frame, text=_(
            "Add Invoice"), command=self.callbacks['create_invoice'])
        add_button.grid(
            column=0, row=14, sticky=tk.W, padx=5, pady=5)

        clear_button = ttk.Button(self.invoice_frame, text=_(
            "Clear Fields"), command=self.clear_all)
        clear_button.grid(
            column=1, row=14, sticky=tk.W, padx=5, pady=5)

    def clear_all(self):
        # clear fields
        for el in self.invoice_form['entry']:
            if isinstance(self.invoice_form['entry'][el], ttk.Entry):
                self.invoice_form['entry'][el].delete(0, tk.END)
            elif isinstance(self.invoice_form['entry'][el], tk.Text):
                self.invoice_form['entry'][el].delete("1.0", tk.END)
            else:
                pass
        self.delete_all_taxes()
        # set defaults again
        self.invoice_form['entry']['currency'].insert(tk.END, 'EUR')
        self.invoice_form['entry']['amount_total']['text'] = "0,00"
        self.invoice_form['combo']['amount_total']['total_pretax']['text'] = "0,00"
        self.invoice_form['combo']['amount_total']['total_tax']['text'] = "0,00"
        self.file_label['text'] = ''
        self.invoice_form['entry']['file'] = ''

        for el in self.booking_form['entry']:
            if isinstance(self.booking_form['entry'][el], ttk.Entry):
                self.booking_form['entry'][el].delete(0, tk.END)
        self.booking_form['entry']['fiscal_period'].insert(
            tk.END, datetime.now().year)
        self.booking_form['treeview'].delete(
            *self.booking_form['treeview'].get_children())

    def select_file(self):
        filetypes = [
            ('Pdf file', '*.pdf')
        ]

        filepath = fd.askopenfilename(
            parent=self.parent,
            title='Open a file',
            initialdir=self.home_path,
            filetypes=filetypes)
        try:
            filename = path.basename(filepath)
        except:
            print("no file choosen!")
            return('break')
        if filename:
            if self.file_label['width'] and len(filename) > self.file_label['width']:
                text = filename[:(self.file_label['width'] // 2) - 2] + \
                    '...' + filename[-((self.file_label['width'] // 2) - 1):]
            self.file_label['text'] = text
            self.invoice_form['entry']['file'] = filepath

    def delete_last_taxes(self):
        if len(self.all_entries) > 1:
            self.all_entries[-1][2].unbind('<KeyRelease>')
            for el in self.all_entries[-1]:
                el.destroy()
            self.all_entries.pop()

    def delete_all_taxes(self):
        for row in self.all_entries:
            row[2].unbind('<KeyRelease>')
            for el in row:
                el.destroy()
        self.all_entries = []
        self.add_more_taxes()

    def add_more_taxes(self):
        next_row = len(self.all_entries)
        row = []
        entry_tax = ttk.Entry(
            self.invoice_form['combo']['taxes']['frame'], width=5)
        if len(self.all_entries) == 0:
            entry_tax.insert(tk.END, '19')
        entry_tax.grid(
            column=2, row=next_row, sticky=tk.E, padx=5, pady=5)
        row.append(entry_tax)
        tax_label = ttk.Label(
            self.invoice_form['combo']['taxes']['frame'], text=_("% of"))
        tax_label.grid(
            column=3, row=next_row, sticky=tk.W, padx=5, pady=5)
        row.append(tax_label)
        entry_amount = ttk.Entry(
            self.invoice_form['combo']['taxes']['frame'])
        entry_amount.grid(
            column=4, row=next_row, sticky=tk.E, padx=5, pady=5)
        row.append(entry_amount)
        tax_amount = ttk.Label(
            self.invoice_form['combo']['taxes']['frame'], text=_("0,00"))
        tax_amount.grid(
            column=5, row=next_row, sticky=tk.W, padx=5, pady=5)
        row.append(tax_amount)
        self.all_entries.append(row)
        self.all_entries[-1][2].bind(
            '<KeyRelease>', lambda event, entries=self.all_entries[-1]: self.form_bind(event, entries))

    def get_taxes(self):
        taxes = {}
        for row in self.all_entries:
            tax = atof(row[2].get() or '0,00')
            tax_amount = Decimal(tax).quantize(
                self.cents, ROUND_HALF_UP)
            taxes[row[0].get()] = float(tax_amount)
        return taxes

    def create_booking_form(self):
        self.booking_frame = tk.LabelFrame(
            self, text=_("Booking Fields"))
        self.booking_frame.grid(
            row=0, column=1, sticky=tk.N + tk.W + tk.S + tk.E, padx=5, pady=5)

        self.booking_form = {'label': {},
                             'entry': {},
                             'treeview': {}
                             }

        self.booking_form['label']['fiscal_period'] = ttk.Label(
            self.booking_frame, text=_("Fiscal Period") + ":")
        self.booking_form['label']['fiscal_period'].grid(
            column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.booking_form['entry']['fiscal_period'] = ttk.Entry(
            self.booking_frame)
        self.booking_form['entry']['fiscal_period'].insert(
            tk.END, datetime.now().year)
        self.booking_form['entry']['fiscal_period'].grid(
            column=1, row=0, sticky=tk.E, padx=5, pady=5)

        self.booking_form['label']['debit_id'] = ttk.Label(
            self.booking_frame, text=_("Debit Account") + ":", name="debit_id")
        self.booking_form['label']['debit_id'].grid(
            column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.booking_form['entry']['debit_id'] = ttk.Entry(self.booking_frame)
        self.booking_form['entry']['debit_id'].grid(
            column=1, row=1, sticky=tk.E, padx=5, pady=5)

        self.booking_form['label']['credit_id'] = ttk.Label(
            self.booking_frame, text=_("Credit Account") + ":", name="credit_id")
        self.booking_form['label']['credit_id'].grid(
            column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.booking_form['entry']['credit_id'] = ttk.Entry(self.booking_frame)
        self.booking_form['entry']['credit_id'].grid(
            column=1, row=2, sticky=tk.E, padx=5, pady=5)

        self.booking_form['label']['building_id'] = ttk.Label(
            self.booking_frame, text=_("Building") + ":", name="building_id")
        self.booking_form['label']['building_id'].grid(
            column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.booking_form['entry']['building_id'] = ttk.Entry(
            self.booking_frame)
        self.booking_form['entry']['building_id'].grid(
            column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.booking_form['label']['apartment_id'] = ttk.Label(
            self.booking_frame, text=_("Apartment") + ":", name="apartment_id")
        self.booking_form['label']['apartment_id'].grid(
            column=0, row=4, sticky=tk.W, padx=5, pady=5)
        self.booking_form['entry']['apartment_id'] = ttk.Entry(
            self.booking_frame)
        self.booking_form['entry']['apartment_id'].grid(
            column=1, row=4, sticky=tk.E, padx=5, pady=5)

        self.booking_form['treeview'] = ttk.Treeview(
            self.booking_frame)
        self.booking_form['treeview'].grid(
            column=0, row=5, columnspan=2, sticky=tk.N + tk.W + tk.S + tk.E, padx=5, pady=5)

        # Bindings
        keys = ['<Return>', '<KP_Enter>']
        entries = ['debit_id', 'credit_id', 'building_id', 'apartment_id']
        for key in keys:
            for entry in entries:
                self.booking_form['entry'][entry].bind(
                    key, lambda event, entry=entry,
                    callback=self.callbacks[entry]: self.search_entries(event,
                                                                        entry,
                                                                        callback))

    def search_entries(self, event, widget_name, callback):
        entry = event.widget
        typed = entry.get()
        tree = self.booking_form['treeview']
        if widget_name == 'apartment_id':
            headline = _('Apartments')
        elif widget_name == 'building_id':
            headline = _('Buildings')
        elif widget_name == 'debit_id' or widget_name == 'credit_id':
            headline = _('Housing Accounts')
        else:
            raise KeyError
        tree.heading('#0', text=headline, anchor=tk.W)
        if len(typed) < 2:
            print(_("At least two characters!"))
        else:
            results = callback(typed)
            if not results:
                tree.unbind("<ButtonRelease-1>")
                tree.delete(*tree.get_children())
                tree.insert(parent='', index=tk.END, text=_("nothing found!"))
                return("break")
            else:
                self.update_treeview(results, tree)
                tree.bind('<ButtonRelease-1>', lambda event,
                          args=[tree, entry, widget_name]: self.get_tree_selection(event, args))
        return("break")

    def update_treeview(self, data, tree):
        tree.delete(*tree.get_children())
        for idx, row in enumerate(data):
            tree.insert(parent='',
                        index=tk.END,
                        iid=idx,
                        text=f'{row[0]}: {row[1]}',
                        values=(row[0]),
                        open=True)
            if len(row) == 3:
                for apt in row[2]:
                    tree.insert(parent=idx, index=tk.END,
                                text=f'{apt.id}: {apt.name}',
                                values=(row[0], apt.id))
        return("break")

    def get_tree_selection(self, event, args):
        curItem = args[0].focus()
        values = args[0].item(curItem)['values']
        if not values:
            return
        args[1].delete(0, tk.END)
        args[1].insert(
            0, values[0])
        if len(values) == 1:
            if args[2] == 'apartment_id':
                self.booking_form['entry']['building_id'].delete(0, tk.END)
            self.booking_form['entry']['apartment_id'].delete(0, tk.END)
            args[1].delete(0, tk.END)
            args[1].insert(0, values[0])

        if len(values) == 2:
            args[1].delete(0, tk.END)
            self.booking_form['entry']['apartment_id'].delete(0, tk.END)
            args[1].insert(0, values[0])
            self.booking_form['entry']['apartment_id'].insert(
                0, values[1])

    # invoice form methods

    def form_bind(self, event, entries):
        try:
            tax = atof(
                entries[0].get() or '0')
            input = atof(
                entries[2].get() or '0,00')
        except ValueError:
            print(_("Decimals only!"))
            return

        new_input = Decimal(input)
        new_input = new_input.quantize(self.cents, ROUND_HALF_UP)
        new_tax = new_input * Decimal(tax / 100)
        new_tax = Decimal(new_tax).quantize(self.cents, ROUND_HALF_UP)

        entries[3].config(
            text=str(f'{Decimal(new_tax):n}'))
        total_pretax = atof('0,00')
        total_tax = atof('0,00')
        self.invoice_form['entry']['amount_total']['text'] = "0,00"
        for el in self.all_entries:
            total_pretax += atof(el[2].get() or '0,00')
            total_tax += atof(el[3]['text'])
        amount_total = Decimal(
            total_pretax + total_tax).quantize(self.cents, ROUND_HALF_UP)
        total_pretax = Decimal(
            total_pretax).quantize(self.cents, ROUND_HALF_UP)
        total_tax = Decimal(total_tax).quantize(self.cents, ROUND_HALF_UP)
        self.invoice_form['entry']['amount_total'].config(
            text=str(f'{Decimal(amount_total):n}'))
        self.invoice_form['combo']['amount_total']['total_pretax'].config(
            text=str(f'{Decimal(total_pretax):n}'))
        self.invoice_form['combo']['amount_total']['total_tax'].config(
            text=str(f'{Decimal(total_tax):n}'))

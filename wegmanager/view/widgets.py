import tkinter as tk
from tkinter import ttk, filedialog as fd, Frame, StringVar
from tkcalendar import DateEntry

from os import path


class Combobox:
    def __init__(self, frame, values, row, column, callback):
        self.combobox = None
        self.frame = frame
        self.values = values
        self.row = row
        self.column = column
        self.dict = {}
        self.result = None
        self.setup(callback)

    def setup(self, callback):
        for row in self.values:
            self.dict[row[1]] = row[0]
        self.combobox = ttk.Combobox(self.frame, values=list(
            self.dict.keys()), state='readonly')
        self.combobox.grid(row=self.row, column=self.column,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        self.combobox.bind("<<ComboboxSelected>>",
                           lambda event: self.selected(event, callback))

    def get(self):
        return self.dict[self.combobox.get()]

    def selected(self, event, callback):
        callback = self.dict[self.combobox.get()]


class FormFrame:
    def __init__(self, parent, fields, defaults, callbacks):
        self.parent = parent
        self.defaults = defaults
        self.fields = fields
        self.setup(callbacks)

    def setup(self, callbacks):
        self.inputs = {'label': {},
                       'entry': {}}
        row = 0
        for key, text in self.fields.items():
            if isinstance(text, list):
                self.inputs['label'][key] = ttk.Label(
                    self.parent, text=_(text[1]) + ":")
                self.inputs['label'][key].grid(
                    column=0, row=row, sticky=tk.W, padx=5, pady=5)

                if text[0] == 'date':
                    self.inputs['entry'][key] = DateEntry(self.parent)
                    self.inputs['entry'][key].configure(validate='none')
                    self.inputs['entry'][key].delete(0, "end")
                    self.inputs['entry'][key].grid(
                        column=1, row=row, sticky=tk.E, padx=5, pady=5)

                if text[0] == 'file':
                    self.file_frame = Frame(self.parent)
                    self.file_frame.grid(
                        column=1, row=row, sticky=tk.E, padx=5, pady=5)
                    open_button = ttk.Button(self.file_frame, text=_(
                        "Select a File..."), command=self.select_file)
                    open_button.grid(
                        column=0, row=0, sticky=tk.E, padx=5, pady=5)
                    self.file_label = tk.Label(
                        self.file_frame, width=20, text="")
                    self.file_label.grid(
                        column=0, row=1, sticky=tk.E, padx=5, pady=5)

                if text[0] == 'custom':
                    elements = callbacks['form_' + key](key, text[1])
                    self.inputs['label'][key] = elements['label'][key]
                    self.inputs['label'][key].grid(
                            column=0, row=row, sticky=tk.W, padx=5, pady=5)
                    for el in elements['entry'][key]:
                        self.inputs['entry'][key] = {}
                        self.inputs['entry'][key][el] = elements['entry'][key][el]
                        if el == 'frame':
                            self.inputs['entry'][key]['frame'].grid(
                                    column=1, row=row, sticky=tk.E, padx=5, pady=5)
                    row += 1

            else:
                self.inputs['label'][key] = ttk.Label(
                    self.parent, text=_(text) + ":")
                self.inputs['label'][key].grid(
                    column=0, row=row, sticky=tk.W, padx=5, pady=5)
                self.inputs['entry'][key] = ttk.Entry(
                    self.parent)
                if key in self.defaults:
                    self.inputs['entry'][key].insert(
                        tk.END, self.defaults[key])
                self.inputs['entry'][key].grid(
                    column=1, row=row, sticky=tk.E, padx=5, pady=5)
            row += 1

        # add button
        add_button = callbacks['add_button']
        add_button.grid(
            column=0, row=row, sticky=tk.E, padx=5, pady=5)

    def select_file(self):
        filetypes = [
            ('Pdf file', '*.pdf')
        ]

        filepath = fd.askopenfilename(
            parent=self.parent,
            title='Open a file',
            initialdir=self.defaults['home_path'],
            filetypes=filetypes)
        filename = path.basename(filepath)
        if filename and self.file_label['width'] and len(filename) > self.file_label['width']:
            text = filename[:(self.file_label['width'] // 2) - 2] + \
                '...' + filename[-((self.file_label['width'] // 2) - 1):]
        self.file_label['text'] = text

import tkinter as tk
from tkinter import ttk


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
        callback['bank_id'] = self.dict[self.combobox.get()]

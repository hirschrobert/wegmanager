import tkinter as tk

from wegmanager.view.AbstractTab import AbstractTab


class Reports(AbstractTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self is Reports, which is an AbstractTab which is a Frame
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_buttons()

    def create_buttons(self):
        self.exportButton = tk.Button(self)
        self.exportButton["text"] = _("export")
        self.exportButton.grid(row=0, column=0, sticky=tk.W)

from tkinter import ttk
import tkinter as tk
from view.Transactions import Transactions
from controller.TransactionController import TransactionController
from .DbController import Base, engine
import gettext
from configparser import ConfigParser
import os
from pprint import pprint


class Application(ttk.Notebook):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # window
        self.parent.group(parent)
        self.grid(row=0, column=0, sticky=tk.N + tk.S +
                  tk.E + tk.W)  # self is ttk.Notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.createConfig()
        self.i18n()

        Base.metadata.create_all(
            bind=engine, checkfirst=True)  # @UndefinedVariable
        self.new_tab(view=Transactions, controller=TransactionController(
        ), name=_("Bank Transactions"))
        #self.new_tab(view=Table, controller=AccountsController(), name=_("Bank Accounts"))
        self.mainloop()

    def new_tab(self, controller, view, name: str):
        view = view(self)
        controller.bind(view)
        self.add(view, text=name)

    def createConfig(self):
        self.config_object = ConfigParser()

        self.config_object["SETUP"] = {
            "language": "de",
        }

        self.config_object["SQLITE"] = {
            "path": "hello/world",
        }

        # create file if not exist and write above config
        with open(os.path.join(os.path.dirname(__file__), '../../data', 'config.ini'), 'w+') as conf:
            self.config_object.write(conf)

    def i18n(self):
        # find . -type f \( -name '*.py' \) -print > locale/filelist # inside main project folder
        # xgettext --files-from=locale/filelist --from-code=utf-8 -p locale/
        # msginit -i locale/messages.pot --locale=de_DE.utf-8 -o locale/de/LC_MESSAGES/messages.po
        # msgfmt locale/de/LC_MESSAGES/messages.po -o locale/de/LC_MESSAGES/messages.mo
        
        i18n = gettext.translation(
            'messages', '../locale', [self.config_object['SETUP']['language']])
        i18n.install()

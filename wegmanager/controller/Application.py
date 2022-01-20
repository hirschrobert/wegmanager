from tkinter import ttk
import tkinter as tk
from wegmanager.view.Transactions import Transactions
from wegmanager.view.Invoices import Invoices
from wegmanager.controller.TransactionController import TransactionController
from wegmanager.controller.InvoiceController import InvoiceController
from wegmanager.controller.DbController import Base, open_db
import gettext
from configparser import ConfigParser
import os
import pkg_resources


class Application(ttk.Notebook):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # window
        self.parent.group(parent)
        self.grid(row=0, column=0, sticky=tk.N + tk.S +
                  tk.E + tk.W)  # self is ttk.Notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.config = self.createConfig()
        self.i18n()
        db_session = self.start_db()

        self.new_tab(view=Transactions, controller=TransactionController(
            db_session), name=_("Bank Transactions"))
        self.new_tab(view=Invoices, controller=InvoiceController(
            db_session), name=_("Invoices"))
        self.mainloop()

    def start_db(self):
        db_path = os.path.join(self.config['SQLITE']['path'], 'db.sqlite')

        # return Base, SessionLocal(), engine
        SessionLocal, engine = open_db(db_path)

        Base.metadata.create_all(  # @UndefinedVariable
            bind=engine, checkfirst=True)

        return SessionLocal

    def new_tab(self, controller, view, name: str):
        view = view(self)
        controller.bind(view)
        self.add(view, text=name)

    def get_home_path(self):
        home_folder = os.getenv('HOME')
        return home_folder

    def createConfig(self):
        # TODO: check if already present
        config_object = ConfigParser()

        config_object["SETUP"] = {
            "language": "de",
        }

        config_object["SQLITE"] = {
            "path": "/var/opt/wegmanager/database",
        }

        # create file if not exist and write above config
        # /usr/lib/wegmanager/config/config.ini

        # might not work with Win and/or Mac

        home_folder = self.get_home_path()
        config_path = os.path.join(home_folder, '.config', 'wegmanager')
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        with open(os.path.join(config_path, 'config'), 'w+') as conf:
            config_object.write(conf)
        return config_object

    def i18n(self):
        # find . -type f \( -name '*.py' \) -print > locale/filelist # inside main project folder
        # xgettext --files-from=locale/filelist --from-code=utf-8 -p locale/
        # msginit -i locale/messages.pot --locale=de_DE.utf-8 -o locale/de/LC_MESSAGES/messages.po
        # msgfmt locale/de/LC_MESSAGES/messages.po -o locale/de/LC_MESSAGES/messages.mo
        # localepath = pkg_resources.resource_filename('wegmanager', 'locale')
        try:
            localepath = pkg_resources.resource_filename(
                'wegmanager', 'locale')
            i18n = gettext.translation(
                'messages', localepath, [self.config['SETUP']['language']])
            i18n.install()
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

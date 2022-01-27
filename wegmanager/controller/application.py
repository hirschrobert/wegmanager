# pylint: disable=missing-module-docstring
import os
import gettext
from configparser import ConfigParser

from tkinter import ttk
import tkinter as tk

import pkg_resources

from wegmanager.view.transactions import Transactions
from wegmanager.view.Invoices import Invoices
from wegmanager.controller.transaction_controller import TransactionController
from wegmanager.controller.InvoiceController import InvoiceController
from wegmanager.controller.db_controller import Dtb


class Application(ttk.Notebook):  # pylint: disable=too-many-ancestors
    '''
    Main Application class that defines the detailed application features.
    It inherits from ttk.Notebook and starts the individual tabs.
     '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # window
        self.parent.group(parent)
        self.grid(row=0, column=0, sticky=tk.N + tk.S +
                  tk.E + tk.W)  # self is ttk.Notebook
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.config = self.create_config()
        self.i18n()

        self.dtb = Dtb(self.get_db_path())

        self.new_tab(view=Transactions, controller=TransactionController(
            self.dtb), name=_("Bank Transactions"))
        self.new_tab(view=Invoices, controller=InvoiceController(
            self.dtb), name=_("Invoices"))
        self.mainloop()

    def get_db_path(self):
        '''
        Starts the connection to the database.
         '''

        db_path = os.path.join(self.config['SQLITE']['path'], 'db.sqlite')

        return db_path

    def new_tab(self, controller, view, name: str):
        '''
        Binds controller and view for a new tab.
        '''

        view = view(self)
        controller.bind(view)
        self.add(view, text=name)

    @staticmethod
    def get_home_path():
        '''
        Get $(HOME) Path of user. Currently linux only.
        '''

        home_folder = os.getenv('HOME')
        return home_folder

    def create_config(self):
        '''
        Use values from config file. Create config file if not exist.
        '''

        config_object = ConfigParser()

        # might not work with Win and/or Mac
        home_folder = self.get_home_path()
        config_path = os.path.join(home_folder, '.config', 'wegmanager')
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        config_path_file = os.path.join(config_path, 'config')
        if os.path.isfile(config_path_file):
            config_object.read(config_path_file)
        else:

            config_object["SETUP"] = {
                "language": "de",
            }

            config_object["SQLITE"] = {
                "path": "/var/opt/wegmanager/database",
            }
            with open(os.path.join(config_path, 'config'),
                      'w+',
                      encoding='utf-8') as conf:
                config_object.write(conf)
        return config_object

    def i18n(self):
        '''
        Setup gettext translation
        '''

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
        except FileNotFoundError as err:
            print(f"Files for translation not found: {err.filename}!")

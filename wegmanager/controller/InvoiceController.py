from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.view.Invoices import Invoices


class InvoiceController(AbstractController):
    def __init__(self, db_session) -> None:
        super().__init__()
        self.view = None
        self.model = None
        self.db_session = db_session

    def bind(self, view: Invoices):
        self.view = view  # notebook

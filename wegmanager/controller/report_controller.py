from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.view.invoices import Invoices
from wegmanager.model.business_partner import BusinessPartner
from wegmanager.model.building import Building


class ReportController(AbstractController):
    def __init__(self, dtb, config) -> None:
        super().__init__()
        self.view = None
        self.model = None
        self.dtb = dtb
        self.config = config

    def bind(self, view: Invoices):
        self.view = view  # notebook
        self.view.exportButton.configure(command=self.export)

    def export(self, typed):
        print('Hello World')
        with db_session() as dtb:
            results = dtb.query(Building)
        if typed.isdigit():
            results = results.filter(
                BusinessPartner.housing_account_id.like(
                    f'%{typed}%')
            )
        else:
            results = results.filter(
                BusinessPartner.name.like(
                    f'%{typed}%')
            )
        return results

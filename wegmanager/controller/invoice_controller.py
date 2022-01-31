from faker import Faker
import random
from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.view.invoices import Invoices

from wegmanager.model.business_partner import BusinessPartner
from wegmanager.model.invoice import Invoice


class InvoiceController(AbstractController):
    def __init__(self, dtb) -> None:
        super().__init__()
        self.view = None
        self.model = None
        self.dtb = dtb

    def bind(self, view: Invoices):
        self.view = view  # notebook
        self.view.exportButton.configure(command=self.export)

    def export(self):
        print('hello')
        faker = Faker()
        lst = list(range(10))
        business_partners = []
        for _ in range(50):
            business_partners.append(BusinessPartner(faker.name()))
        invoices = []
        print(business_partners[2].name)

        # for val in sorted(lst, key=lambda _: random.random()):
        #    invoices.append(Invoice(
        #        debitor=business_partners[val].id,
        #        creditor=business_partners[val + 3].id,
        #        description=faker.sentence(nb_words=10)))

        with self.dtb.get_session() as dtb:
            dtb.add_all(business_partners)
            dtb.commit()

            print(business_partners[0].id)
            inv = Invoice(description=faker.sentence(nb_words=10),
                          debitor_id=business_partners[0].id,
                          creditor_id=business_partners[3].id)
            dtb.add(inv)
            dtb.commit()

from wegmanager.controller.abstract_controller import AbstractController
from wegmanager.view.invoices import Invoices

from wegmanager.model.business_partner import BusinessPartner
from wegmanager.model.invoice import Invoice
from wegmanager.model.housing_account import HousingAccount

from wegmanager.controller import db_session
from wegmanager.model.building import Building
from wegmanager.model.apartment import Apartment
from tkinter import Entry, Text
from locale import atof
from tkcalendar.dateentry import DateEntry


class InvoiceController(AbstractController):
    def __init__(self, dtb, home_path, config) -> None:
        super().__init__()
        self.view = None
        self.model = None
        self.dtb = dtb
        self.home_path = home_path
        self.config = config
        self.callbacks = {}

    def bind(self, view: Invoices):
        self.view = view  # notebook
        self.view.callbacks = {'debit_id': self.search_housing_account,
                               'credit_id': self.search_housing_account,
                               'building_id': self.search_building,
                               'apartment_id': self.search_apartment,
                               'create_invoice': self.create_invoice}
        self.view.create_invoice_form(self.home_path)
        self.view.create_booking_form()

    def create_invoice(self):
        invoice_entries = self.view.invoice_form['entry']
        booking_entries = self.view.booking_form['entry']
        invoice_entries['taxes'] = self.view.get_taxes()
        print(invoice_entries['taxes'])
        invoice = self.validate_invoice_inputs(invoice_entries)
        booking = self.validate_invoice_inputs(booking_entries)
        inv = Invoice(**invoice)
        inv.bookit([booking])

        try:
            invoice_id = self.dtb.setData(inv)
            self.view.clear_all()
        except BaseException as err:
            print(_(f'Could not save to database: {err=}, {type(err)=}'))
            #del self.view.invoice_form['entry']
            #del self.view.booking_form['entry']
            # gc.collect()

    def validate_invoice_inputs(self, entries):
        # TODO: implement validation!
        validated = {}
        for key in entries:
            if isinstance(entries[key], Entry) and not isinstance(entries[key], DateEntry):
                validated[key] = entries[key].get()
            elif isinstance(entries[key], Text):
                validated[key] = entries[key].get("1.0", "end")
            elif key == 'amount_total':
                validated[key] = atof(entries[key]['text'])
            elif isinstance(entries[key], DateEntry):
                validated[key] = entries[key].get_date()
            elif key == 'file':
                validated[key] = entries[key]
                print(validated[key])
            else:
                validated[key] = entries[key]

        return validated

    def search_housing_account(self, typed):
        with db_session() as dtb:
            # results = dtb.query(HousingAccount.id,
            #                    HousingAccount.name)
            results = dtb.query(HousingAccount)
        if typed.isdigit():
            results = results.filter(
                HousingAccount.id.like(
                    f'%{typed}%')
            )
        else:
            results = results.filter(HousingAccount.business_partner.has(
                BusinessPartner.name.like(f'%{typed}%')) | HousingAccount.name.like(f'%{typed}%'))
        #return results
        return [(r.id, r.name) for r in results]

    def search_building(self, typed):
        with db_session() as dtb:
            results = dtb.query(Building)
        if typed.isdigit():
            results = results.filter(
                Building.id.like(
                    f'%{typed}%')
            )
        else:
            results = results.filter(
                Building.name.like(
                    f'%{typed}%')
            )
        return [(r.id, r.name, r.apartments) for r in results]
        # return results

    def search_apartment(self, typed):
        with db_session() as dtb:
            results = dtb.query(Apartment).filter(
                Apartment.building_id.is_(None))
        if typed.isdigit():
            results = results.filter(
                Apartment.id.like(
                    f'%{typed}%')
            )
        else:
            results = results.filter(
                Apartment.name.like(
                    f'%{typed}%')
            )
        return [(r.id, r.name) for r in results]

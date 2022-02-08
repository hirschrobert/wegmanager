from sqlalchemy import (Column, Integer, DATE, VARCHAR,
                        CHAR, NVARCHAR, DATETIME, Float,
                        JSON, String, text)
from sqlalchemy.orm import relationship, validates

from datetime import date

from wegmanager.model import Base
from wegmanager.model.booking import Booking


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)

    # transactions_audited = relationship(
    #    "TransactionAudited", secondary="bookings", back_populates="invoices")

    bookings = relationship(
        "Booking", back_populates="invoice")

    invoice_date = Column(DATE, nullable=True, server_default=text('NULL'))
    date_registered = Column(
        DATE, nullable=True, server_default=text('NULL'))
    invoice_number = Column(NVARCHAR)
    description = Column(NVARCHAR)
    currency = Column(CHAR(3))
    taxes = Column(JSON())
    amount_total = Column(Float(), default=0.0)
    amount_handyman = Column(Float(), default=0.0)
    amount_material = Column(Float(), default=0.0)
    date_service_beginn = Column(
        DATE, nullable=True, server_default=text('NULL'))
    date_service_end = Column(DATE, nullable=True, server_default=text('NULL'))
    status = Column(String(10))
    notes = Column(VARCHAR)
    file = Column(VARCHAR(255))

    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v)
                           for k, v in self.__dict__.items()),
        )

    @validates('amount_total', 'amount_handyman', 'amount_material')
    def validate_amount(self, key, amount):
        if amount == '':
            return 0.0
            #raise ValueError("failed simple email validation")
        return amount

    def bookit(self, bookings):
        for book in bookings:
            self.bookings.append(Booking(invoice=self,
                                         fiscal_period=book['fiscal_period'],
                                         debit_id=book['debit_id'],
                                         credit_id=book['credit_id'],
                                         building_id=book['building_id'],
                                         apartment_id=book['apartment_id']))

    @staticmethod
    def headers():
        headers = {'debitor': _('Debitor'),
                   'creditor': _('Creditor'),
                   'description': _('Description')
                   }
        return headers

    @staticmethod
    def form_fields():
        '''
        0: Type, 1: Text
        '''
        fields = {'invoice_date': ['date', _('Invoice Date')],
                  'date_registered': ['date', _('Date Registered')],
                  'invoice_number': _('Invoice Number'),
                  'description': _('Description'),
                  'currency': _('Currency'),
                  'amount_pretax': _('Amount before tax'),
                  'taxes': ['custom', _('Taxes')],
                  'amount_total': _('Total Amount'),
                  'amount_handyman': _('Amount handyman salary'),
                  'amount_material': _('Amount costs material'),
                  'date_service_beginn': ['date', _('Date Service begins')],
                  'date_service_end': ['date', _('Date Service ends')],
                  'status': _('Status'),
                  'notes': _('Notes'),
                  'file': ['file', _('Invoice PDF File')],
                  }
        return fields

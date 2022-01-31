from sqlalchemy import (Column, Integer, DATE, VARCHAR,
                        CHAR, NVARCHAR, DATETIME, Float,
                        JSON, String, ForeignKey)

from wegmanager.model import Base


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)

    debitor_id = Column(Integer, ForeignKey('business_partners.id'))
    creditor_id = Column(Integer, ForeignKey('business_partners.id'))

    invoice_date = Column(DATE)
    datetime_registered = Column(DATETIME)
    description = Column(NVARCHAR)
    currency = Column(CHAR(3))
    taxes = Column(JSON())
    amount_pretax = Column(Float())
    amount_handyman = Column(Float())
    amount_material = Column(Float())
    invoice_number = Column(NVARCHAR)
    date_service_beginn = Column(DATE)
    date_service_end = Column(DATE)
    status = Column(String(10))
    notes = Column(VARCHAR)

    def __init__(self, description=None, debitor_id=None, creditor_id=None):
        self.description = description
        self.debitor_id = debitor_id
        self.creditor_id = creditor_id

    @staticmethod
    def headers():
        headers = {'debitor': _('Debitor'),
                   'creditor': _('Creditor'),
                   'description': _('Description')
                   }
        return headers

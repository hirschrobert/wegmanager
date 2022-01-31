from sqlalchemy import (Column, Integer, VARCHAR, NVARCHAR, DATETIME,
                        Float, String, JSON, BOOLEAN)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from wegmanager.model import Base


class BusinessPartner(Base):
    __tablename__ = "business_partners"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    street = Column(DATETIME)
    zip_code = Column(NVARCHAR)
    city = Column(Float())
    state = Column(JSON())
    country = Column(JSON())
    notes = Column(VARCHAR)
    is_client = Column(BOOLEAN)
    email = Column(String(50))

    debitors = relationship(
        "Invoice", foreign_keys="Invoice.debitor_id", backref="debitor")
    creditors = relationship(
        "Invoice", foreign_keys="Invoice.creditor_id", backref="creditor")

    @hybrid_property
    def invoices(self):
        return self.debitors.union(self.creditors)

    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def headers():
        headers = {'iban': _('IBAN'),
                   'username': _('Username')
                   }
        return headers

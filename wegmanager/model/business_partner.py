from sqlalchemy import Column, Integer, DATE, VARCHAR, NVARCHAR, DATETIME, Float, JSON
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class BusinessPartner(Base):
    __tablename__ = "business_partners"
    id = Column(Integer, primary_key=True)
    name = Column(DATE)
    street = Column(DATETIME)
    zip_code = Column(NVARCHAR)
    city = Column(Float())
    state = Column(JSON())
    #invoices = relationship("Invoice", back_populates="business_partner")
    # contact_person
    #notes = Column(VARCHAR)

    @staticmethod
    def headers():
        headers = {'iban': _('IBAN'),
                   'username': _('Username')
                   }
        return headers


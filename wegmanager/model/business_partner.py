from sqlalchemy import (Column, Integer, VARCHAR, NVARCHAR, DATETIME,
                        Float, String, JSON, BOOLEAN, ForeignKey)
from sqlalchemy.orm import relationship

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

    housing_account_id = Column(Integer, ForeignKey(
        'housing_accounts.id'), unique=True)

    # many-to-one side remains, see tip below
    housing_account = relationship(
        "HousingAccount", back_populates="business_partner")

    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def headers():
        headers = {'iban': _('IBAN'),
                   'username': _('Username')
                   }
        return headers

from sqlalchemy import Column, String, Integer, VARCHAR
from sqlalchemy.orm import relationship
from wegmanager.model import Base


class HousingAccount(Base):
    __tablename__ = "housing_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    type = Column(VARCHAR(10))
    business_partner = relationship(
        "BusinessPartner", back_populates="housing_account", uselist=False)

    def __init__(self, id=None, name=None, type=None):
        self.id = id
        self.name = name
        self.type = type

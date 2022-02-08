from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    landlord = Column(Integer, ForeignKey(
        'business_partners.id'))

    apartments = relationship("Apartment", back_populates="building")

    def __init__(self, name=None, landlord=None):
        self.name = name
        self.landlord = landlord

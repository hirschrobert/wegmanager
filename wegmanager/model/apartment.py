from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Apartment(Base):
    __tablename__ = "apartments"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    landlord = Column(Integer, ForeignKey(
        'business_partners.id'))

    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship("Building", back_populates="apartments")

    def __init__(self, name=None, landlord=None, building=None):
        self.name = name
        self.landlord = landlord
        self.building = building

from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    name_alt = Column(String(60))
    bic = Column(String(11))
    finurl = Column(String(60))
    custom_fints = Column(JSON())

    bank_users = relationship("BankUser", back_populates="bank")

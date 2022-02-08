from sqlalchemy import (Column, Integer, ForeignKey, DATE, CHAR, func)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Booking(Base):
    '''
    Intermediate associations class serving for a many to many relationship.
    It connects one Invoice to many Booking (left side) and one Transaction_Audited
    to many Booking (right side).
    '''
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False,
                       server_default=func.now())
    user = Column(CHAR(50))
    fiscal_period = Column(Integer)

    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    invoice = relationship("Invoice", back_populates="bookings")

    transaction_audited_id = Column(Integer, ForeignKey(
        'transactions_audited.id'))
    transaction_audited = relationship(
        "TransactionAudited", back_populates="bookings")

    credit_id = Column(Integer, ForeignKey(
        'housing_accounts.id'))
    debit_id = Column(Integer, ForeignKey(
        'housing_accounts.id'))
    building_id = Column(Integer, ForeignKey(
        'buildings.id'))
    apartment_id = Column(Integer, ForeignKey(
        'apartments.id'))

    def __init__(self, user=None, fiscal_period=None, invoice=None,
                 transaction_audited=None, credit_id=None, debit_id=None,
                 building_id=None, apartment_id=None):
        self.user = user
        self.fiscal_period = fiscal_period
        self.invoice = invoice
        self.transaction_audited = transaction_audited
        self.credit_id = credit_id
        self.debit_id = debit_id
        self.building_id = building_id
        self.apartment_id = apartment_id

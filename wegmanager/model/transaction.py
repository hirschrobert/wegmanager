from sqlalchemy import Column, Integer, CHAR, DATETIME, JSON, ForeignKey
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    hash = Column(CHAR(128), unique=True)
    date_retreived = Column(DATETIME)
    json_original = Column(JSON())

    bank_user_id = Column(Integer, ForeignKey('bank_users.id'), nullable=False)
    bank_user = relationship("BankUser", back_populates="transactions")

    transaction_audited = relationship("TransactionAudited",
                                       back_populates="transaction",
                                       foreign_keys='[TransactionAudited.transaction_id]',
                                       uselist=False)

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

    transaction_audited = relationship("TransactionAudited", back_populates="transaction", foreign_keys='[TransactionAudited.transaction_id]', uselist=False)

    @staticmethod
    def headers():
        headers = {'account_iban': _('Own IBAN'),
                   'date': _('Date'),
                   'applicant_name': _('Partner Name'),
                   'applicant_iban': _('Partner IBAN'),
                   'applicant_bin': _('Partner BIC'),
                   'applicant_creditor_id': _('Partner ID'),
                   'purpose': _('Purpose'),
                   'amount': _('Amount'),
                   'currency': _('Currency'),
                   'customer_reference': _('Customer Reference'),
                   'end_to_end_reference': _('End to End Reference'),
                   }
        return headers

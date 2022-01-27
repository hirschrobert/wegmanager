from sqlalchemy import Column, String, Integer, ForeignKey, Table, select
from sqlalchemy.orm import relationship

from wegmanager.model import Base
from wegmanager.model.bank import Bank


class BankUser(Base):
    __tablename__ = "bank_users"
    id = Column(Integer, primary_key=True)
    blz = Column(Integer())
    username = Column(String(25))
    pin = Column(String(25))
    iban = Column(String(34))

    bank = relationship("Bank", back_populates="bank_users")
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)

    transactions = relationship(
        "Transaction", back_populates="bank_user")

    @staticmethod
    def headers():
        headers = {'iban': _('IBAN'),
                   'username': _('Username'),
                   'bank_name': _('Bank name')
                   }
        return headers

    @staticmethod
    def get_selectables():
        table = BankUser().__table__
        banks = Bank().__table__
        selectable = select([
            table.c.id.label("id"),
            table.c.iban.label("iban"),
            table.c.username.label("username"),
            banks.c.name.label("bank_name")
        ]).select_from(table.join(banks)).where(banks.c.id == table.c.bank_id)
        return selectable

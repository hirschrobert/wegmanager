from sqlalchemy import (ForeignKey, Column, String,
                        Integer, DATE, NVARCHAR, Float, CHAR, select, inspect)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement
from sqlalchemy.sql import table

from wegmanager.model import Base
from wegmanager.model.transaction import Transaction
from wegmanager.model.bank_user import BankUser


class TransactionAudited(Base):
    __tablename__ = "transactions_audited"
    id = Column(Integer, primary_key=True)
    #account_iban = Column(String(34))
    date = Column(DATE)
    applicant_name = Column(String(50))
    applicant_iban = Column(String(34))
    applicant_bin = Column(String(8))
    applicant_creditor_id = Column(String(50))
    purpose = Column(NVARCHAR)
    amount = Column(Float())
    currency = Column(CHAR(3))
    customer_reference = Column(String(50))
    end_to_end_reference = Column(String(50))

    transaction_id = Column(Integer, ForeignKey(
        'transactions.id'), unique=True)

    # many-to-one side remains, see tip below
    transaction = relationship(
        "Transaction", back_populates="transaction_audited", foreign_keys='[TransactionAudited.transaction_id]')

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

    @staticmethod
    def get_selectables():
        table = TransactionAudited().__table__
        transacton_table = Transaction().__table__
        bank_users_table = BankUser().__table__
        selectable = select([
            bank_users_table.c.iban.label("account_iban"),
            table.c.date.label("date"),
            table.c.applicant_name.label("applicant_name"),
            table.c.applicant_iban.label("applicant_iban"),
            table.c.applicant_bin.label("applicant_bin"),
            table.c.applicant_creditor_id.label("applicant_creditor_id"),
            table.c.purpose.label("purpose"),
            table.c.amount.label("amount"),
            table.c.currency.label("currency"),
            table.c.customer_reference.label("customer_reference"),
            table.c.end_to_end_reference.label("end_to_end_reference"),
        ]).select_from(table.join(transacton_table).join(bank_users_table)).where(bank_users_table.c.id == transacton_table.c.bank_user_id)
        return selectable


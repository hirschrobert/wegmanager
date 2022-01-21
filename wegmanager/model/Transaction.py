from sqlalchemy import (Column, String, Integer, Float,
                        CHAR, DATE, DATETIME, JSON)
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.sqltypes import NVARCHAR

from wegmanager.controller.db_controller import Base, get_db


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    hash = Column(CHAR(128))
    account_iban = Column(String(34))
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
    date_retreived = Column(DATETIME)
    json_original = Column(JSON())

    def headers(self):
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

    def getModeledData(self, db_session):
        results = self.modelData(db_session)
        headers = self.headers()
        return headers, results

    # TODO
    def modelData(self, db_session):
        results = []
        db = get_db(db_session)
        data = db.query(Transaction).all()
        # if table is empty
        if not data:
            return [{}]
        for row in data:
            results.append({c.key: getattr(row, c.key)
                            for c in inspect(row).mapper.column_attrs})
        return results

    def setData(self, db_session, data):
        db = get_db(db_session)
        db.add(data)
        db.commit()

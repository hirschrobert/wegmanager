from sqlalchemy import Column, Integer, DATE, VARCHAR, NVARCHAR, DATETIME, Float, JSON
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from wegmanager.model import Base


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    invoice_date = Column(DATE)
    datetime_registered = Column(DATETIME)
    description = Column(NVARCHAR)
    amount_pretax = Column(Float())
    taxes = Column(JSON())
    amount_handyman = Column(Float())
    amount_material = Column(Float())
    invoice_number = Column(NVARCHAR)
    #creditor = relationship("BusinessPartner", back_populates="invoices", uselist=False)
    #debitor = relationship("BusinessPartner", back_populates="invoices", uselist=False)
    date_service_beginn = Column(DATE)
    date_service_end = Column(DATE)
    #skr_account = 
    #housing_account = 
    #project_1
    #project_2
    #notes = Column(VARCHAR)
    
    @staticmethod
    def headers(self):
        headers = {'iban': _('IBAN'),
                   'username': _('Username')
                   }
        return headers

    def getModeledData(self, db_session):
        results = self.modelData(db_session)
        headers = self.headers()
        return headers, results

    def setData(self, db_session, data):
        db = get_db(db_session)
        db.add(data)
        db.commit()

    # TODO
    def modelData(self, db_session):
        results = []
        db = get_db(db_session)
        data = db.query(BankUser).all()
        # if table is empty
        if not data:
            return [{}]
        for row in data:
            results.append({c.key: getattr(row, c.key)
                            for c in inspect(row).mapper.column_attrs})
        return results

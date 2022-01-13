from controller.DbController import Base, get_db
from sqlalchemy import Column, String, Integer
from sqlalchemy.inspection import inspect


class BankUser(Base):
    __tablename__ = "bank_user"
    id = Column(Integer, primary_key=True)
    blz = Column(Integer())
    username = Column(String(25))
    pin = Column(String(25))
    finurl = Column(String(60))
    iban = Column(String(34))

    def headers(self):
        headers = {'iban': _('IBAN'),
                   'username': _('Username')
                   }
        return headers

    def getModeledData(self):
        results = self.modelData()
        headers = self.headers()
        return headers, results

    def setData(self, data):
        db = get_db()
        db.add(data)
        db.commit()

    # TODO
    def modelData(self):
        results = []
        db = get_db()
        data = db.query(BankUser).all()
        # if table is empty
        if not data:
            return [{}]
        for row in data:
            results.append({c.key: getattr(row, c.key)
                            for c in inspect(row).mapper.column_attrs})
        return results

import json
import os

from sqlalchemy import create_engine, Table, exc, event, inspect
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table
from sqlalchemy.ext import compiler
from sqlalchemy.engine import Engine

from wegmanager.model import Base
from wegmanager.model.transaction_audited import TransactionAudited
from wegmanager.model.bank_user import BankUser
from wegmanager.controller import db_session


class Dtb:
    def __init__(self, path):
        self.engine = None
        self.open_db(path)
        self.check_bank_attributes()

    def open_db(self, path):
        '''
        Constructs database connection. Creates tables if not exist.
        '''

        conn_str = ''.join(['sqlite:///', path])
        self.engine = create_engine(conn_str, echo=True)
        db_session.configure(bind=self.engine)

        # init views
        self.view_test(TransactionAudited())
        self.view_test(BankUser())

        Base.metadata.create_all(  # @UndefinedVariable
            bind=self.engine, checkfirst=True)

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


    def check_bank_attributes(self):
        table = Table('banks', Base.metadata, autoload_with=self.engine)
        with db_session() as dtb:
            if not dtb.query(table).first():
                try:
                    file = os.path.join('data', 'bank_attributes.json')
                    with open(file, encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        with dtb.get_bind().connect() as connection:
                            connection.execute(table.insert(), data)
                except RuntimeError:
                    print(
                        f'Could not insert initial bank attributes to database.')

    def get_db(self):
        '''
        Getter to provide database connection.
        '''

        try:
            dtb = db_session()
            return dtb
        finally:
            dtb.close()

    def get_session(self):
        '''
        Return the database session, instead of using the global variable
        'db_session()'. Session needs to be closed manually!
        '''
        return db_session()

    def getModeledData(self, model):
        results = self.modelData(model)
        try:
            headers = model.headers()
            return headers, results
        except:
            return results

    # TODO
    def modelData(self, model):
        results = []
        name = str(model.__table__.name) + "_view"
        my_view = Table(name, Base.metadata, autoload_with=self.engine)
        with db_session() as dtb:
            data = dtb.query(my_view).all()
        # if table is empty
        if not data:
            return [{}]
        return [r._asdict() for r in data]
        # for row in data:
        #    results.append({c.key: getattr(row, c.key)
        #                    for c in inspect(row).mapper.column_attrs})
        # return results
        # return data

    def get_data(self, model):
        #table = model.__table__
        with db_session() as dtb:
            data = dtb.query(model).all()
        return data

    def get_by_id(self, model, id):
        with db_session() as dtb:
            data = dtb.query(model).get(id)
        return data

    def get_column_data(self, *columns):
        with db_session() as dtb:
            data = dtb.query(*columns).all()
        return data

    def setData(self, data):
        try:
            with db_session() as dtb:
                dtb.add(data)
                dtb.flush()
                id = data.id
                dtb.commit()
        except exc.SQLAlchemyError as err:
            raise
        return id

    def view_test(self, tmodel):
        # create view
        #name = (type(tmodel).__name__).lower() + "_view"
        name = str(tmodel.__table__.name) + "_view"
        if inspect(self.engine).has_table(name):
            with db_session() as conn:
                conn.execute(f"drop view {name}")
        selectables = tmodel.get_selectables()
        transaction_table_view = self.view(name,
                                           Base.metadata,
                                           selectables)
        return transaction_table_view
        #my_view = Table(name, Base.metadata, autoload_with=self.engine)
        # return my_view

    def view(self, name, metadata, selectable):
        t = table(name)

        for c in selectable.c:
            c._make_proxy(t)

        event.listen(metadata, "after_create", CreateView(name, selectable))
        event.listen(metadata, "before_drop", DropView(name))
        return t


class CreateView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


class DropView(DDLElement):
    def __init__(self, name):
        self.name = name


@compiler.compiles(CreateView)
def compile(element, compiler, **kw):
    return "CREATE VIEW %s AS %s" % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


@compiler.compiles(DropView)
def compile(element, compiler, **kw):
    return "DROP VIEW %s" % (element.name)

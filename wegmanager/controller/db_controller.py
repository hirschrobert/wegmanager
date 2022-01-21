from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def open_db(path):
    '''
    Constructs database connection. Creates tables if not exist.
    '''

    conn_str = ''.join(['sqlite:///', path])
    engine = create_engine(conn_str, connect_args={"check_same_thread": False})
    session_local = sessionmaker(autocommit=False, autoflush=False,
                                 bind=engine)

    return session_local(), engine


def get_db(session):
    '''
    Getter to provide database connection.
    '''

    try:
        dtb = session
        return dtb
    finally:
        dtb.close()

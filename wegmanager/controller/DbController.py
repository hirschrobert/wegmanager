from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()


def open_db(path):
    conn_str = ''.join(['sqlite:///', path])
    engine = create_engine(conn_str, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal(), engine


def get_db(session):
    try:
        db = session
        return db
    finally:
        db.close()

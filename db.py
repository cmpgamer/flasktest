from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import session

Base = declarative_base()
m_testengine = None

def init_db(uri):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import StudentModel
    m_testengine = create_engine(uri, convert_unicode=True)

    Base.metadata.create_all(bind=m_testengine)

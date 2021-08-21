from __future__ import annotations
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String

from .dbconfig import config_by_name

# NOTE: since this is not a flask app, do not use `flask_sqlalchemy`
# https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#setting-alternate-search-paths-on-connect
db_config = config_by_name["test"]
engine = create_engine(db_config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# https://www.fullstackpython.com/sqlalchemy-model-examples.html
Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

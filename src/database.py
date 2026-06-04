###
# This file:
#   creates the SQLite connection
#   creates the SQLAlchemy session
#   initializes tables
#
# All database models inherit from this.
###

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///hospital.db"

# create DB connection
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

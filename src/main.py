###
# main.py
###

from database import engine, Base
from models import Patient, Encounter

Base.metadata.create_all(bind=engine)

print("Database tables created.")
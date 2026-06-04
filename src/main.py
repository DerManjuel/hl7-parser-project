###
# main.py
###


from database import engine, Base, SessionLocal
from models import Patient, Encounter
from hl7_service import process_hl7_message

Base.metadata.create_all(bind=engine)

with open("data/sample_adt_a08.hl7") as file:
    message = file.read()

db = SessionLocal()

patient = process_hl7_message(message, db)

print(f"Processed patient: {patient.first_name} {patient.last_name}")

###
# This layer:
#   coordinates parser + database
#   contains business logic
###

from parser import parse_hl7_message
from models import Patient, Encounter

def process_hl7_message(message, db_session):

    data = parse_hl7_message(message)

    patient = db_session.get(Patient, data["patient_id"])

    if not patient:

        patient = Patient(
            patient_id=data["patient_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            dob=data["dob"],
            sex=data["sex"]
        )

        db_session.add(patient)

    else:

        patient.first_name = data["first_name"]
        patient.last_name = data["last_name"]

    encounter = Encounter(
        patient_id=data["patient_id"],
        attending_doctor=data["attending_doctor"],
        patient_class=data["patient_class"]
    )

    db_session.add(encounter)

    db_session.commit()

    return patient

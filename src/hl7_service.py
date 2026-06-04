###
# This layer:
#   coordinates parser + database
#   contains business logic
###

from parser import parse_hl7_message
from models import Patient, Encounter, ProcessedMessage

def process_hl7_message(message, db_session):

    data = parse_hl7_message(message)

    # ------------------------------------
    # Check duplicate message
    # ------------------------------------

    existing_message = db_session.get(ProcessedMessage, data["message_control_id"])
    if existing_message:
        print("Message already processed")
        return None
    
    # ------------------------------------
    # Patient upsert
    # ------------------------------------

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
        print("Patient updated")

    # ------------------------------------
    # Encounter upsert
    # ------------------------------------

    existing_encounter = (db_session.query(Encounter).filter_by(visit_number=data["visit_number"]).first())
    if existing_encounter:
        existing_encounter.attending_doctor = (data["attending_doctor"])
        existing_encounter.patient_class = (data["patient_class"])
        print("Encounter updated")

    else:
        new_encounter = Encounter(
            visit_number=data["visit_number"],
            patient_id=data["patient_id"],
            attending_doctor=data["attending_doctor"],
            patient_class=data["patient_class"]
        )
        db_session.add(new_encounter)

    # ------------------------------------
    # Mark message as processed
    # ------------------------------------

    processed_message = ProcessedMessage(message_control_id=data["message_control_id"])

    db_session.add(processed_message)

    # ------------------------------------
    # Commit everything
    # ------------------------------------

    db_session.commit()

    return patient

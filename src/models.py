###
# This file defines:
#   tables
#   columns
#   relationships
#
# SQLAlchemy-Modelle für die Datenbanktabellen.
###

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    sex = Column(String)


class Encounter(Base):
    __tablename__ = "encounters"

    encounter_id = Column(Integer, primary_key=True, autoincrement=True)

    visit_number = Column(String, unique=True)

    patient_id = Column(String, ForeignKey("patients.patient_id"))

    attending_doctor = Column(String)

    patient_class = Column(String)


class ProcessedMessage(Base):
    __tablename__ = "processed_messages"

    message_control_id = Column(
        String,
        primary_key=True
    )

from src.parser import parse_hl7_message
from datetime import datetime, date


def test_parse_patient_name():

    message = """
PID|1||100001^^^HOSPITAL^MR||Doe^John||19800115|M
"""

    data = parse_hl7_message(message)

    assert data["patient_id"] == "100001"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


def test_parse_dob():

    message = """
PID|1||100001^^^HOSPITAL^MR||Doe^John||19800115|M
"""

    data = parse_hl7_message(message)

    assert data["dob"] == date(1980, 1, 15)


def test_parse_attending_doctor():

    message = """
PV1|1|I|WARD^101^1||||1234^Smith^Jane
"""

    data = parse_hl7_message(message)

    assert data["attending_doctor"] == "Jane Smith"


def test_missing_pv1_segment():

    message = """
PID|1||100001^^^HOSPITAL^MR||Doe^John||19800115|M
"""

    data = parse_hl7_message(message)

    assert "attending_doctor" not in data


def test_missing_patient_name():

    message = """
PID|1||100001^^^HOSPITAL^MR||||19800115|M
"""

    data = parse_hl7_message(message)

    assert data is not None

def test_missing_patient_name_detailed():

    message = """
PID|1||100001^^^HOSPITAL^MR||||19800115|M
"""

    data = parse_hl7_message(message)

    assert data["first_name"] is None
    assert data["last_name"] is None


def test_partial_patient_name():

    message = """
PID|1||100001^^^HOSPITAL^MR||Doe^||19800115|M
"""

    data = parse_hl7_message(message)

    assert data["last_name"] == "Doe"
    assert data["first_name"] is None
    

def test_parse_message_control_id():

    message = """
MSH|^~\\&|EPIC|HOSPITAL|LAB|HOSPITAL|202505011230||ADT^A08|MSG00001|P|2.5
"""

    data = parse_hl7_message(message)

    assert data["message_control_id"] == "MSG00001"


def test_parse_visit_number():

    message = """
PV1|1|I|WARD^101^1||||1234^Smith^Jane||||||||||||V12345
"""

    data = parse_hl7_message(message)

    assert data["visit_number"] == "V12345"


def test_short_pv1_does_not_crash():

    message = """
PV1|1|I
"""

    data = parse_hl7_message(message)

    assert data["patient_class"] == "I"


def test_full_adt_a08_message():

    message = """
MSH|^~\\&|EPIC|HOSPITAL|LAB|HOSPITAL|202505011230||ADT^A08|MSG00001|P|2.5
PID|1||100001^^^HOSPITAL^MR||Doe^John||19800115|M
PV1|1|I|WARD^101^1||||1234^Smith^Jane||||||||||||V12345
"""

    data = parse_hl7_message(message)

    assert data["patient_id"] == "100001"
    assert data["first_name"] == "John"
    assert data["attending_doctor"] == "Jane Smith"
    assert data["visit_number"] == "V12345"


def test_broken_message_does_not_crash():

    message = "THIS IS NOT HL7"

    data = parse_hl7_message(message)

    assert data is not None


def test_empty_message():

    data = parse_hl7_message("")

    assert data is not None

###
# This file:
#   parses the HL7 v2 message
#   extracts and returns patient and encounter data
###

from datetime import datetime

def parse_hl7_message(message):

    segments = message.strip().split("\n")
    # print(f"DEBUG: Segmente im HL7-Nachricht: {segments}")

    parsed_data = {}

    for segment in segments:

        fields = segment.split("|")

        segment_type = fields[0]

        if segment_type == "PID":

            parsed_data["patient_id"] = fields[3].split("^")[0]

            name = fields[5].split("^")

            parsed_data["last_name"] = name[0]

            parsed_data["first_name"] = name[1]

            parsed_data["dob"] = datetime.strptime(fields[7], "%Y%m%d").date()

            parsed_data["sex"] = fields[8]

        elif segment_type == "PV1":

            doctor = fields[7].split("^")

            parsed_data["attending_doctor"] = f"{doctor[2]} {doctor[1]}"

            parsed_data["patient_class"] = fields[2]

    return parsed_data
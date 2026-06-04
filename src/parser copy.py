# parser.py

import os
import sqlite3

# Eine typische HL7 v2 ADT-Nachricht (Patientenaufnahme) als Text-String
hl7_message = "MSH|^~\\&|EPIC|HOSPITAL|LAB|CLINIC|20260603||ADT^A08|MSG00001|P|2.3|\nPID|1||PATID1234^^^MRN||DOE^JOHN^PID||19900101|M"

# Pfad zur HL7-Testdatei und zur SQLite-Datenbank
HL7_FILE_PATH = "hl7-samples-main/ADT/1632738177-A01.txt"
DB_FILE_PATH = "healthcare.db"


def init_database():
    """Erstellt die SQLite-Datenbank und die Patiententabelle, falls nicht vorhanden."""
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    
    # Erstelle eine einfache SQL-Tabelle für Demografiedaten
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


def parse_hl7_file(file_path):
    """Liest die HL7-Datei ein und extrahiert den Patienten."""
    if not os.path.exists(file_path):
        print(f"Fehler: Datei '{file_path}' nicht gefunden.")
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Segmente trennen (oft mit \n oder \r separiert)
    segments = content.replace('\r', '\n').split('\n')
    
    for segment in segments:
        fields = segment.split('|')
        if fields[0] == 'PID':
            # HL7-Felder sicher extrahieren (Indices anpassen falls nötig)
            patient_id = fields[3].split('^')[0] if len(fields) > 3 else "Unknown"
            
            name_part = fields[5].split('^') if len(fields) > 5 else ["Unknown", "Unknown"]
            last_name = name_part[0] if len(name_part) > 0 else "Unknown"
            first_name = name_part[1] if len(name_part) > 1 else "Unknown"
            
            dob = fields[7] if len(fields) > 7 else "Unknown"
            gender = fields[8] if len(fields) > 8 else "Unknown"
            
            return {
                "PatientID": patient_id,
                "FirstName": first_name,
                "LastName": last_name,
                "DOB": dob,
                "Gender": gender
            }
    return None


def save_patient_to_db(patient):
    """Speichert die extrahierten Daten in der SQLite-Datenbank ab."""
    if not patient:
        return
        
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    
    # Fügt den Patienten ein; falls die ID existiert, werden die Daten überschrieben (UPSERT)
    cursor.execute('''
        INSERT INTO patients (patient_id, first_name, last_name, dob, gender)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(patient_id) DO UPDATE SET
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            dob=excluded.dob,
            gender=excluded.gender
    ''', (patient["PatientID"], patient["FirstName"], patient["LastName"], patient["DOB"], patient["Gender"]))
    
    conn.commit()
    conn.close()
    print(f"Erfolg: Patient {patient['FirstName']} {patient['LastName']} in Datenbank gespeichert!")


# Hauptprogramm starten
if __name__ == "__main__":
    # 1. Datenbank vorbereiten
    init_database()
    
    # 2. Datei parsen
    parsed_data = parse_hl7_file(HL7_FILE_PATH)
    
    # 3. In Datenbank sichern
    if parsed_data:
        save_patient_to_db(parsed_data)
        
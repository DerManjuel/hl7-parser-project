# HL7 v2 Parser Project

## HL7 v2
### Struktur
 - Segmente aus MSH, PID & PV1
 - Felder getrennt durch |
 - Komponenten innerhalb eines Feldes getrennt durch ^

 MSH beinhaltet Header
 PID ist Patienten Segment

## Schritte
 1. Datei öffnen und gesamten Inhalt lesen
 2. \r durch \n ersetzen und dann am Zeilenumbruch splitten:
    HL7-Dateien trennen Segmente oft mit \r, manchmal auch mit \n
 3. Jedes Segment mit | splitten
 4. Wenn das Segment mit PID beginnt, werden Felder extrahiert

## Wichtige Einschränkungen
 Der Code ist sehr einfach und hat einige Limitierungen:

 - er verarbeitet nur PID
 - er ignoriert MSH-Encoding, z. B. wenn Feldtrenner anders sind
 - er geht davon aus, dass das HL7-Format sauber ist
 - er nutzt keine HL7-Bibliothek, sondern nur einfache String-Splits
 - er behandelt nur die erste PID-Zeile in der Datei
 
Daher sind HL7-Bibliotheken sinnvoll.
Bspw.: hl7apy, python-hl7 & simple-hl7.

## ToDo
HL7 Message File‚
      ↓
HL7 Parser
      ↓
Validation Layer
      ↓
SQLite/PostgreSQL
      ↓
CLI Query Tool

## Structure

hl7v2-patient-parser/
│
├── data/
│   └── sample_adt_a08.hl7
│
├── src/
│   ├── parser.py
│   ├── database.py
│   ├── models.py
│   ├── hl7_service.py
│   └── main.py
│
├── tests/
│   └── test_parser.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── architecture.png

## Runthrough

main.py
   ↓
hl7_service.py
   ↓
parser.py  → extracts HL7 fields
   ↓
models.py  → defines DB structure
   ↓
database.py → creates DB connection/session
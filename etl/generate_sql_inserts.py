"""
DM Lab Experiment 1: SQL Insert Generator
Translates synthetic CSV datasets into pure SQL INSERT statements for sql/05_load_sample_data.sql.
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")

def parse_date_id(date_str):
    parts = date_str.split("-")
    if len(parts[0]) == 4:  # YYYY-MM-DD
        y, m, d = parts[0], parts[1], parts[2]
    else:  # DD-MM-YYYY
        d, m, y = parts[0], parts[1], parts[2]
    return int(f"{int(y):04d}{int(m):02d}{int(d):02d}"), f"{y}-{int(m):02d}-{int(d):02d}", int(m), f"Q{(int(m)-1)//3 + 1}", int(y)

def main():
    lines = [
        "-- =============================================================================",
        "-- DM Lab Experiment 1: Healthcare Data Warehouse",
        "-- Script 05: Load Sample Data via SQL Inserts",
        "-- Allows direct SQL execution independent of Python ETL",
        "-- =============================================================================\n",
        "USE healthcare_dw;\n"
    ]

    # 1. Dim_Patient
    lines.append("-- 1. Populate Dim_Patient")
    with open(os.path.join(DATA_DIR, "patients.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = "Female" if row["gender"].strip().upper().startswith("F") else "Male"
            lines.append(f"INSERT INTO Dim_Patient (Patient_ID, Name, Gender, Age, City) VALUES ('{row['patient_id']}', '{row['name']}', '{g}', {row['age']}, '{row['city']}');")
    lines.append("")

    # 2. Dim_Doctor
    lines.append("-- 2. Populate Dim_Doctor")
    with open(os.path.join(DATA_DIR, "doctors.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lines.append(f"INSERT INTO Dim_Doctor (Doctor_ID, Name, Specialization, Experience_Years) VALUES ('{row['doctor_id']}', '{row['name']}', '{row['specialization']}', {row['experience_years']});")
    lines.append("")

    # 3. Dim_Hospital & Dim_Location & Dim_Hospital_Snowflake
    lines.append("-- 3. Populate Dim_Hospital & Dim_Location & Dim_Hospital_Snowflake")
    loc_id = 1
    with open(os.path.join(DATA_DIR, "hospitals.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lid = f"LOC{loc_id:03d}"
            loc_id += 1
            lines.append(f"INSERT INTO Dim_Location (Location_ID, City, State, Country, Region) VALUES ('{lid}', '{row['location']}', '{row['state']}', '{row['country']}', '{row['region']}');")
            lines.append(f"INSERT INTO Dim_Hospital (Hospital_ID, Hospital_Name, Location, Type) VALUES ('{row['hospital_id']}', '{row['hospital_name']}', '{row['location']}', '{row['type']}');")
            lines.append(f"INSERT INTO Dim_Hospital_Snowflake (Hospital_ID, Hospital_Name, Location_ID, Type) VALUES ('{row['hospital_id']}', '{row['hospital_name']}', '{lid}', '{row['type']}');")
    lines.append("")

    # 4. Dim_Date & Fact_Patient_Visit & Fact_Patient_Visit_Snowflake
    lines.append("-- 4. Populate Dim_Date and Fact_Patient_Visit")
    dates_seen = {}
    visit_inserts = []
    visit_sn_inserts = []
    with open(os.path.join(DATA_DIR, "patient_visits.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did, d_str, m, q, y = parse_date_id(row["visit_date"])
            if did not in dates_seen:
                dates_seen[did] = (d_str, m, q, y)
            visit_inserts.append(f"INSERT INTO Fact_Patient_Visit (Visit_ID, Patient_ID, Doctor_ID, Hospital_ID, Date_ID, Diagnosis, Treatment_Cost, Visit_Duration_Minutes) VALUES ('{row['visit_id']}', '{row['patient_id']}', '{row['doctor_id']}', '{row['hospital_id']}', {did}, '{row['diagnosis']}', {row['treatment_cost']}, {row['visit_duration_minutes']});")
            visit_sn_inserts.append(f"INSERT INTO Fact_Patient_Visit_Snowflake (Visit_ID, Patient_ID, Doctor_ID, Hospital_ID, Date_ID, Diagnosis, Treatment_Cost, Visit_Duration_Minutes) VALUES ('{row['visit_id']}', '{row['patient_id']}', '{row['doctor_id']}', '{row['hospital_id']}', {did}, '{row['diagnosis']}', {row['treatment_cost']}, {row['visit_duration_minutes']});")

    for did in sorted(dates_seen.keys()):
        d_str, m, q, y = dates_seen[did]
        lines.append(f"INSERT INTO Dim_Date (Date_ID, Date, Month, Quarter, Year) VALUES ({did}, '{d_str}', {m}, '{q}', {y});")
    lines.append("")

    lines.extend(visit_inserts)
    lines.append("")
    lines.extend(visit_sn_inserts)
    lines.append("")

    # 5. Dim_Medication & Fact_Medication_Records
    lines.append("-- 5. Populate Dim_Medication & Fact_Medication_Records")
    with open(os.path.join(DATA_DIR, "medications.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lines.append(f"INSERT INTO Dim_Medication (Medication_ID, Medication_Name, Category, Unit_Cost) VALUES ('{row['medication_id']}', '{row['medication_name']}', '{row['category']}', {row['unit_cost']});")
    lines.append("")

    with open(os.path.join(DATA_DIR, "medication_records.csv"), "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did, _, _, _, _ = parse_date_id(row["prescription_date"])
            lines.append(f"INSERT INTO Fact_Medication_Records (Medication_Record_ID, Patient_ID, Doctor_ID, Date_ID, Medication_ID, Dosage_MG, Units_Prescribed, Total_Medication_Cost) VALUES ('{row['medication_record_id']}', '{row['patient_id']}', '{row['doctor_id']}', {did}, '{row['medication_id']}', {row['dosage_mg']}, {row['units_prescribed']}, {row['total_medication_cost']});")

    out_file = os.path.join(SQL_DIR, "05_load_sample_data.sql")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated {out_file} successfully.")

if __name__ == "__main__":
    main()

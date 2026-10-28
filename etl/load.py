"""
DM Lab Experiment 1: ETL Warehouse Loader
Loads transformed dimensional and fact records into the data warehouse.
Supports both MySQL (production lab engine) and SQLite (zero-setup portable engine)
with parameterized SQL and foreign-key safe execution ordering.
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load configuration from .env if present
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_ENGINE = os.getenv("DB_ENGINE", "mysql").lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "healthcare_dw")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
SQLITE_DB_PATH = os.path.join(BASE_DIR, os.getenv("SQLITE_DB_PATH", "healthcare_dw.db"))

class WarehouseConnection:
    """Manages database connection and dialect differences between MySQL and SQLite."""

    def __init__(self, engine: str = DB_ENGINE):
        self.engine = engine
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.engine == "mysql":
            import mysql.connector
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                buffered=True
            )
            self.cursor = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(SQLITE_DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self._ensure_sqlite_tables()
        return self

    def _ensure_sqlite_tables(self):
        """Creates tables in SQLite if they do not exist."""
        ddl = """
        CREATE TABLE IF NOT EXISTS Dim_Patient (
            Patient_ID TEXT PRIMARY KEY,
            Name TEXT NOT NULL,
            Gender TEXT NOT NULL,
            Age INTEGER NOT NULL,
            City TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Dim_Doctor (
            Doctor_ID TEXT PRIMARY KEY,
            Name TEXT NOT NULL,
            Specialization TEXT NOT NULL,
            Experience_Years INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Dim_Hospital (
            Hospital_ID TEXT PRIMARY KEY,
            Hospital_Name TEXT NOT NULL,
            Location TEXT NOT NULL,
            Type TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Dim_Location (
            Location_ID TEXT PRIMARY KEY,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Country TEXT NOT NULL,
            Region TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Dim_Hospital_Snowflake (
            Hospital_ID TEXT PRIMARY KEY,
            Hospital_Name TEXT NOT NULL,
            Location_ID TEXT NOT NULL,
            Type TEXT NOT NULL,
            FOREIGN KEY (Location_ID) REFERENCES Dim_Location (Location_ID)
        );
        CREATE TABLE IF NOT EXISTS Dim_Date (
            Date_ID INTEGER PRIMARY KEY,
            Date TEXT NOT NULL,
            Month INTEGER NOT NULL,
            Quarter TEXT NOT NULL,
            Year INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Dim_Medication (
            Medication_ID TEXT PRIMARY KEY,
            Medication_Name TEXT NOT NULL,
            Category TEXT NOT NULL,
            Unit_Cost REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Fact_Patient_Visit (
            Visit_ID TEXT PRIMARY KEY,
            Patient_ID TEXT NOT NULL,
            Doctor_ID TEXT NOT NULL,
            Hospital_ID TEXT NOT NULL,
            Date_ID INTEGER NOT NULL,
            Diagnosis TEXT NOT NULL,
            Treatment_Cost REAL NOT NULL,
            Visit_Duration_Minutes INTEGER NOT NULL,
            FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
            FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
            FOREIGN KEY (Hospital_ID) REFERENCES Dim_Hospital (Hospital_ID),
            FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID)
        );
        CREATE TABLE IF NOT EXISTS Fact_Patient_Visit_Snowflake (
            Visit_ID TEXT PRIMARY KEY,
            Patient_ID TEXT NOT NULL,
            Doctor_ID TEXT NOT NULL,
            Hospital_ID TEXT NOT NULL,
            Date_ID INTEGER NOT NULL,
            Diagnosis TEXT NOT NULL,
            Treatment_Cost REAL NOT NULL,
            Visit_Duration_Minutes INTEGER NOT NULL,
            FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
            FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
            FOREIGN KEY (Hospital_ID) REFERENCES Dim_Hospital_Snowflake (Hospital_ID),
            FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID)
        );
        CREATE TABLE IF NOT EXISTS Fact_Medication_Records (
            Medication_Record_ID TEXT PRIMARY KEY,
            Patient_ID TEXT NOT NULL,
            Doctor_ID TEXT NOT NULL,
            Date_ID INTEGER NOT NULL,
            Medication_ID TEXT NOT NULL,
            Dosage_MG INTEGER NOT NULL,
            Units_Prescribed INTEGER NOT NULL,
            Total_Medication_Cost REAL NOT NULL,
            FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
            FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
            FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID),
            FOREIGN KEY (Medication_ID) REFERENCES Dim_Medication (Medication_ID)
        );
        """
        self.cursor.executescript(ddl)
        self.conn.commit()

    def param(self) -> str:
        return "%s" if self.engine == "mysql" else "?"

    def execute_batch(self, query: str, rows: List[tuple]) -> int:
        if not rows:
            return 0
        self.cursor.executemany(query, rows)
        self.conn.commit()
        return len(rows)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def load_warehouse_tables(
    patients: List[Dict[str, Any]],
    doctors: List[Dict[str, Any]],
    star_hospitals: List[Dict[str, Any]],
    locations: List[Dict[str, Any]],
    sn_hospitals: List[Dict[str, Any]],
    dates: List[Dict[str, Any]],
    medications: List[Dict[str, Any]],
    visits: List[Dict[str, Any]],
    prescriptions: List[Dict[str, Any]],
    engine: str = DB_ENGINE
) -> Dict[str, int]:
    """
    Loads all dimensional and fact tables in foreign-key safe order.
    Truncates/clears existing records to ensure idempotency on repeated ETL runs.
    """
    counts = {}

    with WarehouseConnection(engine=engine) as db:
        p = db.param()

        # 1. Truncate / delete existing tables in reverse-dependency order
        tables_to_clear = [
            "Fact_Medication_Records",
            "Fact_Patient_Visit_Snowflake",
            "Fact_Patient_Visit",
            "Dim_Medication",
            "Dim_Hospital_Snowflake",
            "Dim_Location",
            "Dim_Hospital",
            "Dim_Date",
            "Dim_Doctor",
            "Dim_Patient"
        ]
        for tbl in tables_to_clear:
            try:
                db.cursor.execute(f"DELETE FROM {tbl};")
            except Exception:
                pass
        db.conn.commit()

        # 2. Dim_Patient
        patient_rows = [(r["patient_id"], r["name"], r["gender"], r["age"], r["city"]) for r in patients]
        q_patient = f"INSERT INTO Dim_Patient (Patient_ID, Name, Gender, Age, City) VALUES ({p}, {p}, {p}, {p}, {p})"
        counts["Dim_Patient"] = db.execute_batch(q_patient, patient_rows)

        # 3. Dim_Doctor
        doctor_rows = [(r["doctor_id"], r["name"], r["specialization"], r["experience_years"]) for r in doctors]
        q_doctor = f"INSERT INTO Dim_Doctor (Doctor_ID, Name, Specialization, Experience_Years) VALUES ({p}, {p}, {p}, {p})"
        counts["Dim_Doctor"] = db.execute_batch(q_doctor, doctor_rows)

        # 4. Dim_Hospital (Star)
        hosp_rows = [(r["hospital_id"], r["hospital_name"], r["location"], r["type"]) for r in star_hospitals]
        q_hosp = f"INSERT INTO Dim_Hospital (Hospital_ID, Hospital_Name, Location, Type) VALUES ({p}, {p}, {p}, {p})"
        counts["Dim_Hospital"] = db.execute_batch(q_hosp, hosp_rows)

        # 5. Dim_Location (Snowflake)
        loc_rows = [(r["location_id"], r["city"], r["state"], r["country"], r["region"]) for r in locations]
        q_loc = f"INSERT INTO Dim_Location (Location_ID, City, State, Country, Region) VALUES ({p}, {p}, {p}, {p}, {p})"
        counts["Dim_Location"] = db.execute_batch(q_loc, loc_rows)

        # 6. Dim_Hospital_Snowflake
        sn_hosp_rows = [(r["hospital_id"], r["hospital_name"], r["location_id"], r["type"]) for r in sn_hospitals]
        q_sn_hosp = f"INSERT INTO Dim_Hospital_Snowflake (Hospital_ID, Hospital_Name, Location_ID, Type) VALUES ({p}, {p}, {p}, {p})"
        counts["Dim_Hospital_Snowflake"] = db.execute_batch(q_sn_hosp, sn_hosp_rows)

        # 7. Dim_Date
        date_rows = [(r["date_id"], r["date"], r["month"], r["quarter"], r["year"]) for r in dates]
        q_date = f"INSERT INTO Dim_Date (Date_ID, Date, Month, Quarter, Year) VALUES ({p}, {p}, {p}, {p}, {p})"
        counts["Dim_Date"] = db.execute_batch(q_date, date_rows)

        # 8. Dim_Medication
        med_rows = [(r["medication_id"], r["medication_name"], r["category"], r["unit_cost"]) for r in medications]
        q_med = f"INSERT INTO Dim_Medication (Medication_ID, Medication_Name, Category, Unit_Cost) VALUES ({p}, {p}, {p}, {p})"
        counts["Dim_Medication"] = db.execute_batch(q_med, med_rows)

        # 9. Fact_Patient_Visit (Star)
        visit_rows = [
            (r["visit_id"], r["patient_id"], r["doctor_id"], r["hospital_id"], r["date_id"], r["diagnosis"], r["treatment_cost"], r["visit_duration_minutes"])
            for r in visits
        ]
        q_visit = f"INSERT INTO Fact_Patient_Visit (Visit_ID, Patient_ID, Doctor_ID, Hospital_ID, Date_ID, Diagnosis, Treatment_Cost, Visit_Duration_Minutes) VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})"
        counts["Fact_Patient_Visit"] = db.execute_batch(q_visit, visit_rows)

        # 10. Fact_Patient_Visit_Snowflake
        q_sn_visit = f"INSERT INTO Fact_Patient_Visit_Snowflake (Visit_ID, Patient_ID, Doctor_ID, Hospital_ID, Date_ID, Diagnosis, Treatment_Cost, Visit_Duration_Minutes) VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})"
        counts["Fact_Patient_Visit_Snowflake"] = db.execute_batch(q_sn_visit, visit_rows)

        # 11. Fact_Medication_Records (Constellation)
        presc_rows = [
            (r["medication_record_id"], r["patient_id"], r["doctor_id"], r["date_id"], r["medication_id"], r["dosage_mg"], r["units_prescribed"], r["total_medication_cost"])
            for r in prescriptions
        ]
        q_presc = f"INSERT INTO Fact_Medication_Records (Medication_Record_ID, Patient_ID, Doctor_ID, Date_ID, Medication_ID, Dosage_MG, Units_Prescribed, Total_Medication_Cost) VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, {p})"
        counts["Fact_Medication_Records"] = db.execute_batch(q_presc, presc_rows)

    return counts

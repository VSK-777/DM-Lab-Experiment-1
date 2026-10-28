"""
DM Lab Experiment 1: ETL Extraction Module
Safely ingests source CSV files and performs initial structure and schema validation.
"""

import csv
import os
from typing import Dict, List, Tuple

EXPECTED_SCHEMAS = {
    "patients.csv": {"patient_id", "name", "gender", "age", "city"},
    "doctors.csv": {"doctor_id", "name", "specialization", "experience_years"},
    "hospitals.csv": {"hospital_id", "hospital_name", "location", "type", "state", "country", "region"},
    "patient_visits.csv": {"visit_id", "patient_id", "doctor_id", "hospital_id", "visit_date", "diagnosis", "treatment_cost", "visit_duration_minutes"},
    "medications.csv": {"medication_id", "medication_name", "category", "unit_cost"},
    "medication_records.csv": {"medication_record_id", "patient_id", "doctor_id", "prescription_date", "medication_id", "dosage_mg", "units_prescribed", "total_medication_cost"}
}

def extract_csv(filepath: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Extracts records from a CSV file with validation.
    Returns (records, errors).
    """
    if not os.path.exists(filepath):
        return [], [f"File not found: {filepath}"]

    filename = os.path.basename(filepath)
    expected_cols = EXPECTED_SCHEMAS.get(filename)

    records = []
    errors = []

    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return [], [f"Empty CSV file or missing headers: {filepath}"]

            header_set = set(reader.fieldnames)
            if expected_cols and not expected_cols.issubset(header_set):
                missing = expected_cols - header_set
                errors.append(f"Header mismatch in {filename}. Missing required columns: {missing}")
                return [], errors

            for row_num, row in enumerate(reader, start=2):
                # Clean whitespace in keys and values
                cleaned_row = {k.strip(): (v.strip() if v is not None else "") for k, v in row.items() if k}
                records.append(cleaned_row)

    except Exception as e:
        errors.append(f"Extraction error reading {filepath}: {str(e)}")

    return records, errors

def extract_all_sources(data_dir: str) -> Tuple[Dict[str, List[Dict[str, str]]], Dict[str, List[str]]]:
    """
    Extracts all healthcare source datasets from the data directory.
    """
    datasets = {}
    extraction_report = {}

    for filename in EXPECTED_SCHEMAS.keys():
        filepath = os.path.join(data_dir, filename)
        records, errors = extract_csv(filepath)
        datasets[filename] = records
        extraction_report[filename] = {
            "record_count": len(records),
            "errors": errors
        }

    return datasets, extraction_report

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "data")
    data, report = extract_all_sources(data_dir)
    print("ETL Extraction Summary:")
    for fn, rep in report.items():
        print(f"  - {fn}: {rep['record_count']} records extracted. Errors: {len(rep['errors'])}")

"""
DM Lab Experiment 1: Master ETL Pipeline Runner
Executes End-to-End ETL pipeline: Extract -> Transform -> Dimension Key Resolution -> Load.
Provides detailed operational metrics and validation checks.
"""

import os
import sys
import argparse
from typing import Dict, Any

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.extract import extract_all_sources
from etl.transform import HealthcareWarehouseTransformer
from etl.load import load_warehouse_tables, DB_ENGINE

def run_pipeline(engine: str = DB_ENGINE) -> Dict[str, Any]:
    """Runs the full ETL cycle and returns operational metrics."""
    data_dir = os.path.join(BASE_DIR, "data")
    print(f"============================================================")
    print(f"   STARTING HEALTHCARE DATA WAREHOUSE ETL PIPELINE")
    print(f"   Target Database Engine: {engine.upper()}")
    print(f"============================================================")

    # 1. EXTRACT
    print("\n[PHASE 1: EXTRACTION]")
    raw_datasets, extract_report = extract_all_sources(data_dir)
    total_raw_rows = 0
    for filename, rep in extract_report.items():
        cnt = rep["record_count"]
        total_raw_rows += cnt
        err_msg = f" (Errors: {rep['errors']})" if rep['errors'] else ""
        print(f"  -> Extracted {cnt:>3} rows from {filename}{err_msg}")

    # 2. TRANSFORM
    print("\n[PHASE 2: TRANSFORMATION & DATA CLEANSING]")
    transformer = HealthcareWarehouseTransformer()

    patients = transformer.transform_patients(raw_datasets["patients.csv"])
    doctors = transformer.transform_doctors(raw_datasets["doctors.csv"])
    star_hospitals, locations, sn_hospitals = transformer.transform_hospitals(raw_datasets["hospitals.csv"])
    medications = transformer.transform_medications(raw_datasets["medications.csv"])

    valid_patients = {p["patient_id"] for p in patients}
    valid_doctors = {d["doctor_id"] for d in doctors}
    valid_hospitals = {h["hospital_id"] for h in star_hospitals}
    valid_meds = {m["medication_id"] for m in medications}

    visits, date_map = transformer.transform_visits(
        raw_datasets["patient_visits.csv"],
        valid_patients,
        valid_doctors,
        valid_hospitals
    )

    prescriptions = transformer.transform_prescriptions(
        raw_datasets["medication_records.csv"],
        valid_patients,
        valid_doctors,
        valid_meds,
        date_map
    )

    dates = list(date_map.values())

    print(f"  -> Patients cleaned:      {len(patients):>3}")
    print(f"  -> Doctors cleaned:       {len(doctors):>3}")
    print(f"  -> Hospitals (Star):      {len(star_hospitals):>3}")
    print(f"  -> Locations (Snowflake): {len(locations):>3}")
    print(f"  -> Date dimension keys:   {len(dates):>3}")
    print(f"  -> Medications cleaned:   {len(medications):>3}")
    print(f"  -> Visits (Star/Snow):    {len(visits):>3}")
    print(f"  -> Prescriptions (Galaxy):{len(prescriptions):>3}")
    print(f"  -> Duplicates detected:   {transformer.duplicates_detected:>3}")
    print(f"  -> Records rejected:      {len(transformer.rejected_records):>3}")
    if transformer.rejected_records:
        for rej in transformer.rejected_records:
            print(f"     * REJECTED in {rej['source']}: {rej['reason']}")

    # 3. LOAD
    print(f"\n[PHASE 3: LOADING WAREHOUSE TABLES ({engine.upper()})]")
    load_counts = load_warehouse_tables(
        patients=patients,
        doctors=doctors,
        star_hospitals=star_hospitals,
        locations=locations,
        sn_hospitals=sn_hospitals,
        dates=dates,
        medications=medications,
        visits=visits,
        prescriptions=prescriptions,
        engine=engine
    )

    for tbl, count in load_counts.items():
        print(f"  -> Successfully loaded {count:>3} rows into {tbl}")

    print("\n============================================================")
    print("   ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("============================================================\n")

    return {
        "raw_rows_extracted": total_raw_rows,
        "transformed_patients": len(patients),
        "transformed_visits": len(visits),
        "transformed_prescriptions": len(prescriptions),
        "duplicates_detected": transformer.duplicates_detected,
        "rejected_count": len(transformer.rejected_records),
        "loaded_counts": load_counts
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Healthcare Warehouse ETL Pipeline")
    parser.add_argument("--engine", default=DB_ENGINE, choices=["mysql", "sqlite"], help="Database engine to load into")
    args = parser.parse_args()
    run_pipeline(engine=args.engine)

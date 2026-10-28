"""
Unit tests for Healthcare Data Warehouse ETL Transformation Module.
Validates business logic, standardization, data cleansing, and error handling.
Does not require any database connectivity.
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.transform import (
    standardize_gender,
    parse_date_attributes,
    clean_string,
    parse_positive_float,
    parse_positive_int,
    HealthcareWarehouseTransformer
)

class TestTransformationRules:
    """Tests isolated transformation utility functions."""

    def test_standardize_gender_valid(self):
        assert standardize_gender("M") == "Male"
        assert standardize_gender("m") == "Male"
        assert standardize_gender("Male") == "Male"
        assert standardize_gender("M ") == "Male"
        assert standardize_gender("F") == "Female"
        assert standardize_gender("f") == "Female"
        assert standardize_gender("Female") == "Female"
        assert standardize_gender(" F ") == "Female"

    def test_standardize_gender_invalid(self):
        assert standardize_gender("") is None
        assert standardize_gender(None) is None
        assert standardize_gender("Unknown") is None
        assert standardize_gender("123") is None

    def test_parse_date_attributes_iso(self):
        res = parse_date_attributes("2024-03-15")
        assert res is not None
        assert res["date_id"] == 20240315
        assert res["date"] == "2024-03-15"
        assert res["month"] == 3
        assert res["quarter"] == "Q1"
        assert res["year"] == 2024

    def test_parse_date_attributes_dmy(self):
        res = parse_date_attributes("25-08-2024")
        assert res is not None
        assert res["date_id"] == 20240825
        assert res["date"] == "2024-08-25"
        assert res["month"] == 8
        assert res["quarter"] == "Q3"
        assert res["year"] == 2024

    def test_parse_date_attributes_invalid(self):
        assert parse_date_attributes("not-a-date") is None
        assert parse_date_attributes("") is None
        assert parse_date_attributes(None) is None

    def test_clean_string(self):
        assert clean_string("  Apollo   Hospitals  ") == "Apollo Hospitals"
        assert clean_string("") == ""
        assert clean_string(None) == ""

    def test_parse_positive_float(self):
        assert parse_positive_float("1250.50") == 1250.50
        assert parse_positive_float(500) == 500.00
        assert parse_positive_float("0") == 0.00
        assert parse_positive_float("-50.00") is None
        assert parse_positive_float("invalid") is None

    def test_parse_positive_int(self):
        assert parse_positive_int("45") == 45
        assert parse_positive_int("0", strictly_positive=True) is None
        assert parse_positive_int("0", strictly_positive=False) == 0
        assert parse_positive_int("-10") is None
        assert parse_positive_int("abc") is None

class TestWarehouseTransformer:
    """Tests transformer pipeline, duplicate handling, and rejection logging."""

    def setup_method(self):
        self.transformer = HealthcareWarehouseTransformer()

    def test_patient_transformation_and_deduplication(self):
        raw = [
            {"patient_id": "P001", "name": "Aarav Sharma", "gender": "m", "age": "34", "city": "Mumbai"},
            {"patient_id": "P001", "name": "Duplicate Aarav", "gender": "Male", "age": "34", "city": "Mumbai"}, # duplicate ID
            {"patient_id": "P002", "name": "Ananya Patel", "gender": "Female", "age": "28", "city": "Delhi"},
            {"patient_id": "P003", "name": "Bad Age", "gender": "F", "age": "-5", "city": "Pune"}, # invalid age
            {"patient_id": "P004", "name": "Bad Gender", "gender": "X", "age": "40", "city": "Chennai"} # invalid gender
        ]
        clean = self.transformer.transform_patients(raw)
        assert len(clean) == 2
        assert clean[0]["patient_id"] == "P001"
        assert clean[0]["gender"] == "Male"
        assert clean[1]["patient_id"] == "P002"
        assert clean[1]["gender"] == "Female"
        assert self.transformer.duplicates_detected == 1
        assert len(self.transformer.rejected_records) == 2

    def test_visit_referential_integrity_rejection(self):
        valid_patients = {"P001"}
        valid_doctors = {"D001"}
        valid_hospitals = {"H001"}

        raw_visits = [
            # Valid visit
            {"visit_id": "V001", "patient_id": "P001", "doctor_id": "D001", "hospital_id": "H001", "visit_date": "2024-05-10", "diagnosis": "Hypertension", "treatment_cost": "1500", "visit_duration_minutes": "30"},
            # Invalid patient FK
            {"visit_id": "V002", "patient_id": "P999", "doctor_id": "D001", "hospital_id": "H001", "visit_date": "2024-05-10", "diagnosis": "Hypertension", "treatment_cost": "1500", "visit_duration_minutes": "30"},
            # Invalid doctor FK
            {"visit_id": "V003", "patient_id": "P001", "doctor_id": "D999", "hospital_id": "H001", "visit_date": "2024-05-10", "diagnosis": "Hypertension", "treatment_cost": "1500", "visit_duration_minutes": "30"},
            # Negative cost
            {"visit_id": "V004", "patient_id": "P001", "doctor_id": "D001", "hospital_id": "H001", "visit_date": "2024-05-10", "diagnosis": "Hypertension", "treatment_cost": "-500", "visit_duration_minutes": "30"}
        ]

        clean_visits, date_map = self.transformer.transform_visits(
            raw_visits, valid_patients, valid_doctors, valid_hospitals
        )
        assert len(clean_visits) == 1
        assert clean_visits[0]["visit_id"] == "V001"
        assert clean_visits[0]["date_id"] == 20240510
        assert 20240510 in date_map
        assert len(self.transformer.rejected_records) == 3

"""
DM Lab Experiment 1: ETL Transformation Module
Implements business rules, data cleansing, standardization, referential validation,
and multidimensional key generation. Fully unit testable without database dependencies.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

def standardize_gender(gender_str: Optional[str]) -> Optional[str]:
    """
    Standardizes raw gender string to 'Male' or 'Female'.
    Handles values such as M, Male, m, F, Female, f, with trimming.
    Returns None if value cannot be mapped.
    """
    if not gender_str:
        return None
    val = gender_str.strip().upper()
    if val in ("M", "MALE"):
        return "Male"
    if val in ("F", "FEMALE"):
        return "Female"
    return None

def parse_date_attributes(date_str: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Parses date in DD-MM-YYYY or YYYY-MM-DD format.
    Generates smart integer Date_ID (YYYYMMDD), Date string (YYYY-MM-DD),
    Month (1-12), Quarter (Q1-Q4), and Year.
    """
    if not date_str:
        return None
    cleaned = date_str.strip()
    dt = None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(cleaned, fmt)
            break
        except ValueError:
            continue

    if dt is None:
        return None

    month = dt.month
    quarter = f"Q{(month - 1) // 3 + 1}"
    date_id = int(dt.strftime("%Y%m%d"))
    return {
        "date_id": date_id,
        "date": dt.strftime("%Y-%m-%d"),
        "month": month,
        "quarter": quarter,
        "year": dt.year
    }

def clean_string(val: Optional[str]) -> str:
    """Trims whitespace and normalizes text."""
    if val is None:
        return ""
    return " ".join(val.strip().split())

def parse_positive_float(val: Any) -> Optional[float]:
    """Validates and parses nonnegative floating point values (e.g., costs)."""
    try:
        f = float(val)
        return round(f, 2) if f >= 0 else None
    except (ValueError, TypeError):
        return None

def parse_positive_int(val: Any, strictly_positive: bool = True) -> Optional[int]:
    """Validates and parses positive integers (e.g. durations, ages)."""
    try:
        i = int(val)
        if strictly_positive:
            return i if i > 0 else None
        return i if i >= 0 else None
    except (ValueError, TypeError):
        return None

class HealthcareWarehouseTransformer:
    """Transforms extracted raw CSV records into clean dimensional warehouse records."""

    def __init__(self):
        self.rejected_records: List[Dict[str, Any]] = []
        self.duplicates_detected = 0

    def transform_patients(self, raw_patients: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        clean_patients = []
        seen_ids: Set[str] = set()

        for row in raw_patients:
            pid = clean_string(row.get("patient_id"))
            if not pid:
                self.rejected_records.append({"source": "patients", "row": row, "reason": "Missing patient_id"})
                continue
            if pid in seen_ids:
                self.duplicates_detected += 1
                continue
            seen_ids.add(pid)

            name = clean_string(row.get("name"))
            if not name:
                self.rejected_records.append({"source": "patients", "row": row, "reason": "Missing patient name"})
                continue

            gender = standardize_gender(row.get("gender"))
            if not gender:
                self.rejected_records.append({"source": "patients", "row": row, "reason": f"Invalid gender format: {row.get('gender')}"})
                continue

            age = parse_positive_int(row.get("age"), strictly_positive=False)
            if age is None or age > 130:
                self.rejected_records.append({"source": "patients", "row": row, "reason": f"Invalid age: {row.get('age')}"})
                continue

            city = clean_string(row.get("city"))
            if not city:
                self.rejected_records.append({"source": "patients", "row": row, "reason": "Missing city"})
                continue

            clean_patients.append({
                "patient_id": pid,
                "name": name,
                "gender": gender,
                "age": age,
                "city": city
            })
        return clean_patients

    def transform_doctors(self, raw_doctors: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        clean_doctors = []
        seen_ids: Set[str] = set()

        for row in raw_doctors:
            did = clean_string(row.get("doctor_id"))
            if not did:
                self.rejected_records.append({"source": "doctors", "row": row, "reason": "Missing doctor_id"})
                continue
            if did in seen_ids:
                self.duplicates_detected += 1
                continue
            seen_ids.add(did)

            name = clean_string(row.get("name"))
            spec = clean_string(row.get("specialization"))
            exp = parse_positive_int(row.get("experience_years"), strictly_positive=False)
            if exp is None:
                exp = 0

            clean_doctors.append({
                "doctor_id": did,
                "name": name,
                "specialization": spec,
                "experience_years": exp
            })
        return clean_doctors

    def transform_hospitals(self, raw_hospitals: List[Dict[str, str]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Transforms hospital data for:
        1. Star Schema: Dim_Hospital (Hospital_ID, Hospital_Name, Location, Type)
        2. Snowflake Schema: Dim_Location and Dim_Hospital_Snowflake
        """
        clean_star_hospitals = []
        clean_locations = []
        clean_sn_hospitals = []
        seen_hosp_ids: Set[str] = set()
        seen_loc_keys: Dict[Tuple[str, str], str] = {}
        loc_counter = 1

        for row in raw_hospitals:
            hid = clean_string(row.get("hospital_id"))
            if not hid or hid in seen_hosp_ids:
                continue
            seen_hosp_ids.add(hid)

            hname = clean_string(row.get("hospital_name"))
            loc = clean_string(row.get("location"))
            htype = clean_string(row.get("type"))
            state = clean_string(row.get("state", "Unknown"))
            country = clean_string(row.get("country", "India"))
            region = clean_string(row.get("region", "National"))

            clean_star_hospitals.append({
                "hospital_id": hid,
                "hospital_name": hname,
                "location": loc,
                "type": htype
            })

            loc_key = (loc, state)
            if loc_key not in seen_loc_keys:
                lid = f"LOC{loc_counter:03d}"
                loc_counter += 1
                seen_loc_keys[loc_key] = lid
                clean_locations.append({
                    "location_id": lid,
                    "city": loc,
                    "state": state,
                    "country": country,
                    "region": region
                })
            else:
                lid = seen_loc_keys[loc_key]

            clean_sn_hospitals.append({
                "hospital_id": hid,
                "hospital_name": hname,
                "location_id": lid,
                "type": htype
            })

        return clean_star_hospitals, clean_locations, clean_sn_hospitals

    def transform_medications(self, raw_meds: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        clean_meds = []
        seen: Set[str] = set()
        for row in raw_meds:
            mid = clean_string(row.get("medication_id"))
            if not mid or mid in seen:
                continue
            seen.add(mid)
            cost = parse_positive_float(row.get("unit_cost"))
            clean_meds.append({
                "medication_id": mid,
                "medication_name": clean_string(row.get("medication_name")),
                "category": clean_string(row.get("category")),
                "unit_cost": cost if cost is not None else 0.0
            })
        return clean_meds

    def transform_visits(
        self,
        raw_visits: List[Dict[str, str]],
        valid_patients: Set[str],
        valid_doctors: Set[str],
        valid_hospitals: Set[str]
    ) -> Tuple[List[Dict[str, Any]], Dict[int, Dict[str, Any]]]:
        """
        Transforms patient visit records and generates Conformed Date Dimension records.
        Validates referential integrity against dimension keys.
        """
        clean_visits = []
        date_dimension_map: Dict[int, Dict[str, Any]] = {}
        seen_visit_ids: Set[str] = set()

        for row in raw_visits:
            vid = clean_string(row.get("visit_id"))
            if not vid:
                self.rejected_records.append({"source": "visits", "row": row, "reason": "Missing visit_id"})
                continue
            if vid in seen_visit_ids:
                self.duplicates_detected += 1
                continue
            seen_visit_ids.add(vid)

            pid = clean_string(row.get("patient_id"))
            did = clean_string(row.get("doctor_id"))
            hid = clean_string(row.get("hospital_id"))

            # Referential integrity validation
            if pid not in valid_patients:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Foreign key error: patient_id '{pid}' not found"})
                continue
            if did not in valid_doctors:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Foreign key error: doctor_id '{did}' not found"})
                continue
            if hid not in valid_hospitals:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Foreign key error: hospital_id '{hid}' not found"})
                continue

            date_info = parse_date_attributes(row.get("visit_date"))
            if not date_info:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Invalid date: '{row.get('visit_date')}'"})
                continue

            date_id = date_info["date_id"]
            if date_id not in date_dimension_map:
                date_dimension_map[date_id] = date_info

            cost = parse_positive_float(row.get("treatment_cost"))
            if cost is None:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Invalid treatment_cost: '{row.get('treatment_cost')}'"})
                continue

            duration = parse_positive_int(row.get("visit_duration_minutes"), strictly_positive=True)
            if duration is None:
                self.rejected_records.append({"source": "visits", "row": row, "reason": f"Invalid visit_duration_minutes: '{row.get('visit_duration_minutes')}'"})
                continue

            diag = clean_string(row.get("diagnosis", "Unspecified"))

            clean_visits.append({
                "visit_id": vid,
                "patient_id": pid,
                "doctor_id": did,
                "hospital_id": hid,
                "date_id": date_id,
                "diagnosis": diag,
                "treatment_cost": cost,
                "visit_duration_minutes": duration
            })

        return clean_visits, date_dimension_map

    def transform_prescriptions(
        self,
        raw_prescriptions: List[Dict[str, str]],
        valid_patients: Set[str],
        valid_doctors: Set[str],
        valid_meds: Set[str],
        date_dimension_map: Dict[int, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Transforms secondary fact table (Fact_Medication_Records) for constellation schema."""
        clean_prescriptions = []
        seen_ids: Set[str] = set()

        for row in raw_prescriptions:
            mrid = clean_string(row.get("medication_record_id"))
            if not mrid or mrid in seen_ids:
                continue
            seen_ids.add(mrid)

            pid = clean_string(row.get("patient_id"))
            did = clean_string(row.get("doctor_id"))
            mid = clean_string(row.get("medication_id"))

            if pid not in valid_patients or did not in valid_doctors or mid not in valid_meds:
                continue

            date_info = parse_date_attributes(row.get("prescription_date"))
            if not date_info:
                continue
            date_id = date_info["date_id"]
            if date_id not in date_dimension_map:
                date_dimension_map[date_id] = date_info

            dosage = parse_positive_int(row.get("dosage_mg"), strictly_positive=True) or 20
            units = parse_positive_int(row.get("units_prescribed"), strictly_positive=True) or 10
            total_cost = parse_positive_float(row.get("total_medication_cost")) or 100.0

            clean_prescriptions.append({
                "medication_record_id": mrid,
                "patient_id": pid,
                "doctor_id": did,
                "date_id": date_id,
                "medication_id": mid,
                "dosage_mg": dosage,
                "units_prescribed": units,
                "total_medication_cost": total_cost
            })

        return clean_prescriptions

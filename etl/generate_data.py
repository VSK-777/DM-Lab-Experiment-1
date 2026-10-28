"""
DM Lab Experiment 1: Synthetic Healthcare Data Generator
Generates realistic, reproducible synthetic CSV datasets for testing the Healthcare Data Warehouse.
Seed is fixed (42) for deterministic reproduction.
"""

import csv
import os
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Fixed random seed for deterministic dataset generation
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

def generate_hospitals():
    """Generates 5 hospitals with locations and classifications."""
    hospitals = [
        {"hospital_id": "H001", "hospital_name": "Apollo Hospitals", "location": "Mumbai", "type": "Multi-Specialty", "state": "Maharashtra", "country": "India", "region": "West"},
        {"hospital_id": "H002", "hospital_name": "Fortis Hospital", "location": "Mumbai", "type": "Super-Specialty", "state": "Maharashtra", "country": "India", "region": "West"},
        {"hospital_id": "H003", "hospital_name": "Manipal Hospital", "location": "Bangalore", "type": "Multi-Specialty", "state": "Karnataka", "country": "India", "region": "South"},
        {"hospital_id": "H004", "hospital_name": "Max Healthcare", "location": "Delhi", "type": "Super-Specialty", "state": "Delhi", "country": "India", "region": "North"},
        {"hospital_id": "H005", "hospital_name": "AIIMS", "location": "Delhi", "type": "Government Specialty", "state": "Delhi", "country": "India", "region": "North"}
    ]
    filepath = os.path.join(DATA_DIR, "hospitals.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["hospital_id", "hospital_name", "location", "type", "state", "country", "region"])
        writer.writeheader()
        writer.writerows(hospitals)
    print(f"Generated {len(hospitals)} hospitals -> {filepath}")
    return hospitals

def generate_doctors():
    """Generates 10 doctors across clinical specializations."""
    doctors = [
        {"doctor_id": "D001", "name": "Dr. Rajesh Sharma", "specialization": "Cardiology", "experience_years": 16},
        {"doctor_id": "D002", "name": "Dr. Priya Nair", "specialization": "Cardiology", "experience_years": 12},
        {"doctor_id": "D003", "name": "Dr. Amit Verma", "specialization": "Neurology", "experience_years": 14},
        {"doctor_id": "D004", "name": "Dr. Sunita Rao", "specialization": "Neurology", "experience_years": 9},
        {"doctor_id": "D005", "name": "Dr. Vikram Joshi", "specialization": "Orthopedics", "experience_years": 18},
        {"doctor_id": "D006", "name": "Dr. Ananya Sen", "specialization": "Pediatrics", "experience_years": 8},
        {"doctor_id": "D007", "name": "Dr. Rohan Kulkarni", "specialization": "Cardiology", "experience_years": 11},
        {"doctor_id": "D008", "name": "Dr. Meera Iyer", "specialization": "General Medicine", "experience_years": 15},
        {"doctor_id": "D009", "name": "Dr. Suresh Patel", "specialization": "Oncology", "experience_years": 20},
        {"doctor_id": "D010", "name": "Dr. Kavita Menon", "specialization": "Dermatology", "experience_years": 7}
    ]
    filepath = os.path.join(DATA_DIR, "doctors.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["doctor_id", "name", "specialization", "experience_years"])
        writer.writeheader()
        writer.writerows(doctors)
    print(f"Generated {len(doctors)} doctors -> {filepath}")
    return doctors

def generate_patients():
    """Generates 25 patients with raw gender notations for ETL transformation testing."""
    first_names_m = ["Aarav", "Rohan", "Vivaan", "Aditya", "Kabir", "Arjun", "Reyansh", "Muhammad", "Sai", "Vikram", "Rahul", "Karan"]
    first_names_f = ["Ananya", "Diya", "Isha", "Saanvi", "Myra", "Aadhya", "Pooja", "Neha", "Rhea", "Tara", "Tanvi", "Shreya", "Sneha"]
    last_names = ["Sharma", "Patel", "Verma", "Rao", "Nair", "Joshi", "Kulkarni", "Iyer", "Deshmukh", "Mehta", "Gupta", "Reddy"]
    cities = ["Mumbai", "Mumbai", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune"]
    
    # Intentionally vary raw gender format (M, F, Male, Female, m, f) to test ETL standardization
    raw_genders_m = ["M", "Male", "m", "M "]
    raw_genders_f = ["F", "Female", "f", " F"]

    patients = []
    for i in range(1, 26):
        pid = f"P{i:03d}"
        is_female = (i % 2 == 0)
        if is_female:
            name = f"{random.choice(first_names_f)} {random.choice(last_names)}"
            gender = random.choice(raw_genders_f)
        else:
            name = f"{random.choice(first_names_m)} {random.choice(last_names)}"
            gender = random.choice(raw_genders_m)
        age = random.randint(18, 78)
        # Ensure first few patients are from Mumbai for predictable OLAP dice queries
        city = "Mumbai" if i <= 7 else random.choice(cities)
        patients.append({
            "patient_id": pid,
            "name": name,
            "gender": gender,
            "age": age,
            "city": city
        })

    filepath = os.path.join(DATA_DIR, "patients.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["patient_id", "name", "gender", "age", "city"])
        writer.writeheader()
        writer.writerows(patients)
    print(f"Generated {len(patients)} patients -> {filepath}")
    return patients

def generate_medications():
    """Generates medication master dimension records."""
    meds = [
        {"medication_id": "MED001", "medication_name": "Atorvastatin 20mg", "category": "Cardiovascular", "unit_cost": 15.50},
        {"medication_id": "MED002", "medication_name": "Aspirin 75mg", "category": "Antiplatelet", "unit_cost": 4.25},
        {"medication_id": "MED003", "medication_name": "Metformin 500mg", "category": "Antidiabetic", "unit_cost": 6.80},
        {"medication_id": "MED004", "medication_name": "Levetiracetam 500mg", "category": "Neurological", "unit_cost": 32.00},
        {"medication_id": "MED005", "medication_name": "Amoxicillin 500mg", "category": "Antibiotic", "unit_cost": 18.00},
        {"medication_id": "MED006", "medication_name": "Ibuprofen 400mg", "category": "Analgesic", "unit_cost": 8.50},
        {"medication_id": "MED007", "medication_name": "Paracetamol 650mg", "category": "Antipyretic", "unit_cost": 3.50},
        {"medication_id": "MED008", "medication_name": "Telmisartan 40mg", "category": "Antihypertensive", "unit_cost": 22.00}
    ]
    filepath = os.path.join(DATA_DIR, "medications.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["medication_id", "medication_name", "category", "unit_cost"])
        writer.writeheader()
        writer.writerows(meds)
    print(f"Generated {len(meds)} medications -> {filepath}")
    return meds

def generate_visits_and_prescriptions(patients, doctors, hospitals, medications):
    """
    Generates >=60 realistic patient visits with dates spanning 2024 quarters (and 2023 for slice demo).
    Ensures targeted records for:
    - Mumbai patients treated by Cardiologists in 2024 (for DICE)
    - Quarterly distribution across Q1, Q2, Q3, Q4 2024 (for ROLL-UP / DRILL-DOWN)
    - Multiple doctors and hospitals (for PIVOT cross-tabulation)
    """
    diagnoses_by_spec = {
        "Cardiology": ["Coronary Artery Disease", "Hypertension", "Arrhythmia", "Angina Pectoris"],
        "Neurology": ["Migraine", "Epilepsy", "Peripheral Neuropathy", "Tension Headache"],
        "Orthopedics": ["Osteoarthritis", "Lumbar Spondylosis", "Ligament Tear", "Tendinitis"],
        "Pediatrics": ["Viral Fever", "Bronchitis", "Allergic Rhinitis"],
        "General Medicine": ["Type 2 Diabetes", "Upper Respiratory Infection", "Gastroenteritis"],
        "Oncology": ["Colorectal Screening", "Breast Mass Evaluation", "Post-Chemo Followup"],
        "Dermatology": ["Psoriasis", "Atopic Dermatitis", "Acne Vulgaris"]
    }

    visits = []
    prescriptions = []

    # Distribution of dates across 2024 (and a few in 2023 for slice contrast)
    date_schedule = [
        # 2023 historical baseline
        ("15-11-2023", 2023, 11, "Q4"),
        ("20-12-2023", 2023, 12, "Q4"),
        # 2024 Q1
        ("10-01-2024", 2024, 1, "Q1"),
        ("18-01-2024", 2024, 1, "Q1"),
        ("05-02-2024", 2024, 2, "Q1"),
        ("22-02-2024", 2024, 2, "Q1"),
        ("12-03-2024", 2024, 3, "Q1"),
        ("28-03-2024", 2024, 3, "Q1"),
        # 2024 Q2
        ("08-04-2024", 2024, 4, "Q2"),
        ("25-04-2024", 2024, 4, "Q2"),
        ("14-05-2024", 2024, 5, "Q2"),
        ("29-05-2024", 2024, 5, "Q2"),
        ("11-06-2024", 2024, 6, "Q2"),
        ("24-06-2024", 2024, 6, "Q2"),
        # 2024 Q3
        ("07-07-2024", 2024, 7, "Q3"),
        ("21-07-2024", 2024, 7, "Q3"),
        ("15-08-2024", 2024, 8, "Q3"),
        ("28-08-2024", 2024, 8, "Q3"),
        ("10-09-2024", 2024, 9, "Q3"),
        ("26-09-2024", 2024, 9, "Q3"),
        # 2024 Q4
        ("05-10-2024", 2024, 10, "Q4"),
        ("22-10-2024", 2024, 10, "Q4"),
        ("12-11-2024", 2024, 11, "Q4"),
        ("27-11-2024", 2024, 11, "Q4"),
        ("08-12-2024", 2024, 12, "Q4"),
        ("20-12-2024", 2024, 12, "Q4"),
    ]

    visit_counter = 1
    med_counter = 1

    # Deterministic generation of 70 visits
    for idx in range(70):
        vid = f"V{visit_counter:04d}"
        visit_counter += 1

        # Cycle through date schedule
        raw_date, year, month, quarter = date_schedule[idx % len(date_schedule)]
        
        # Format date variety: alternate between DD-MM-YYYY and YYYY-MM-DD to test ETL
        if idx % 3 == 0:
            d_obj = datetime.strptime(raw_date, "%d-%m-%Y")
            formatted_date_input = d_obj.strftime("%Y-%m-%d")
        else:
            formatted_date_input = raw_date

        # Guarantee Dice Query matches: Mumbai patient + Cardiologist + 2024
        if idx < 12:
            # First 12 visits explicitly designed with Mumbai patients and Cardiologists (D001, D002, D007)
            patient = patients[idx % 5]  # P001 - P005 are in Mumbai
            doctor = [d for d in doctors if d["specialization"] == "Cardiology"][idx % 3]
            hospital = [h for h in hospitals if h["location"] == "Mumbai"][idx % 2]
        else:
            patient = patients[idx % len(patients)]
            doctor = doctors[idx % len(doctors)]
            hospital = hospitals[idx % len(hospitals)]

        spec = doctor["specialization"]
        diag = random.choice(diagnoses_by_spec.get(spec, ["General Consultation"]))
        
        cost = round(random.uniform(500.0, 8500.0), 2)
        duration = random.randint(15, 60)

        visits.append({
            "visit_id": vid,
            "patient_id": patient["patient_id"],
            "doctor_id": doctor["doctor_id"],
            "hospital_id": hospital["hospital_id"],
            "visit_date": formatted_date_input,
            "diagnosis": diag,
            "treatment_cost": cost,
            "visit_duration_minutes": duration
        })

        # Add medication record for subset of visits
        if idx % 2 == 0:
            med_rec_id = f"MR{med_counter:04d}"
            med_counter += 1
            med = medications[idx % len(medications)]
            units = random.randint(10, 60)
            total_med_cost = round(units * med["unit_cost"], 2)

            prescriptions.append({
                "medication_record_id": med_rec_id,
                "patient_id": patient["patient_id"],
                "doctor_id": doctor["doctor_id"],
                "prescription_date": formatted_date_input,
                "medication_id": med["medication_id"],
                "dosage_mg": random.choice([20, 40, 75, 100, 500]),
                "units_prescribed": units,
                "total_medication_cost": total_med_cost
            })

    # Save patient_visits.csv
    visits_file = os.path.join(DATA_DIR, "patient_visits.csv")
    with open(visits_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "visit_id", "patient_id", "doctor_id", "hospital_id",
            "visit_date", "diagnosis", "treatment_cost", "visit_duration_minutes"
        ])
        writer.writeheader()
        writer.writerows(visits)
    print(f"Generated {len(visits)} patient visits -> {visits_file}")

    # Save medication_records.csv
    presc_file = os.path.join(DATA_DIR, "medication_records.csv")
    with open(presc_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "medication_record_id", "patient_id", "doctor_id",
            "prescription_date", "medication_id", "dosage_mg",
            "units_prescribed", "total_medication_cost"
        ])
        writer.writeheader()
        writer.writerows(prescriptions)
    print(f"Generated {len(prescriptions)} medication records -> {presc_file}")

    return visits, prescriptions

def main():
    print("Generating reproducible synthetic healthcare warehouse data...")
    hospitals = generate_hospitals()
    doctors = generate_doctors()
    patients = generate_patients()
    medications = generate_medications()
    visits, prescriptions = generate_visits_and_prescriptions(patients, doctors, hospitals, medications)
    print("Synthetic dataset generation completed successfully.")

if __name__ == "__main__":
    main()

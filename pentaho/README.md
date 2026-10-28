# Pentaho Data Integration (PDI / Kettle) Guide

This directory documents how to execute the Healthcare Data Warehouse ETL pipeline using **Pentaho Data Integration (PDI / Kettle)**, as specified in the university lab manual `Exp-1.pdf`.

---

## 1. PDI Installation in Workspace

PDI Community Edition 11.0 is located locally at:
```
C:\Users\Lenovo\Desktop\VSK\B.Tech\3-1\Labs\DM Lab\pdi-ce-11.0.0.0-237\data-integration\
```

To launch the graphical designer (Spoon):
```powershell
cd "C:\Users\Lenovo\Desktop\VSK\B.Tech\3-1\Labs\DM Lab\pdi-ce-11.0.0.0-237\data-integration"
.\Spoon.bat
```

---

## 2. Visual Pipeline Flow (as specified on Page 6 of `Exp-1.pdf`)

```
CSV Input  ──►  Select Values  ──►  Lookup Dimension ID  ──►  Insert into Fact Table
```

### Detailed Pentaho Step Configuration:

1. **CSV File Input Step (`patient_visits.csv`)**:
   - *File:* Browse to `data/patient_visits.csv`.
   - *Delimiter:* `,`
   - *Enclosure:* `"`
   - *Fields:* `visit_id`, `patient_id`, `doctor_id`, `hospital_id`, `visit_date`, `diagnosis`, `treatment_cost`, `visit_duration_minutes`.

2. **Select Values Step**:
   - Set `treatment_cost` to **Number** (Format: `0.00`).
   - Set `visit_duration_minutes` to **Integer**.
   - Set `visit_date` format to `yyyy-MM-dd` or `dd-MM-yyyy`.

3. **Value Mapper Step (Data Cleansing)**:
   - *Target Field:* `gender`
   - *Source values:* `M`, `m`, `Male` $\rightarrow$ Target: `Male`
   - *Source values:* `F`, `f`, `Female` $\rightarrow$ Target: `Female`

4. **Database Lookup Step (`Lookup Dimension ID`)**:
   - Connect to `healthcare_dw`.
   - Lookup `Patient_ID` in table `Dim_Patient`.
   - Lookup `Doctor_ID` in table `Dim_Doctor`.
   - Lookup `Hospital_ID` in table `Dim_Hospital`.
   - Lookup `Date_ID` in table `Dim_Date`.

5. **Table Output Step (`Insert into Fact Table`)**:
   - *Target Table:* `Fact_Patient_Visit`
   - *Commit Size:* 1000
   - Map source stream fields to table columns:
     - `visit_id` $\rightarrow$ `Visit_ID`
     - `patient_id` $\rightarrow$ `Patient_ID`
     - `doctor_id` $\rightarrow$ `Doctor_ID`
     - `hospital_id` $\rightarrow$ `Hospital_ID`
     - `date_id` $\rightarrow$ `Date_ID`
     - `diagnosis` $\rightarrow$ `Diagnosis`
     - `treatment_cost` $\rightarrow$ `Treatment_Cost`
     - `visit_duration_minutes` $\rightarrow$ `Visit_Duration_Minutes`

---

## 3. Pentaho Transformation XML Artifact

A pre-configured PDI XML transformation specification is provided in:
[`healthcare_etl_transform.ktr`](file:///C:/Users/Lenovo/Desktop/VSK/B.Tech/3-1/Labs/DM%20Lab/DM%20LAB-24%20BATCH/DM-Lab-Experiment-1/pentaho/healthcare_etl_transform.ktr)

You can open this file directly in Spoon by navigating to:
**File $\rightarrow$ Open $\rightarrow$ `pentaho/healthcare_etl_transform.ktr`**.

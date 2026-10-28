# Data Warehouse End-to-End Architecture

This document outlines the architectural data flow, component layout, and structural relationships of the **Healthcare Data Warehouse** implemented for DM Lab Experiment 1.

---

## 1. End-to-End Data Pipeline Architecture

```mermaid
flowchart TD
    subgraph Sources["Operational Data Sources (CSV Tier)"]
        S1["patients.csv<br/>(Demographics)"]
        S2["doctors.csv<br/>(Specializations)"]
        S3["hospitals.csv<br/>(Facilities)"]
        S4["patient_visits.csv<br/>(Clinical Encounters)"]
        S5["medications.csv<br/>(Drug Catalog)"]
        S6["medication_records.csv<br/>(Prescriptions)"]
    end

    subgraph ETL["ETL Processing Engine (Python 3 / Pentaho PDI)"]
        E1["extract.py<br/>(Header Validation & Safe Reading)"]
        T1["transform.py<br/>- Gender Standardization<br/>- Date Parsing & Key Gen<br/>- Bounds & Type Checking<br/>- Deduplication"]
        V1["Referential Validator<br/>- Check FK Dimension Keys<br/>- Reject Malformed Rows"]
        L1["load.py<br/>- Foreign Key Safe Loading<br/>- Parameterized SQL Inserts<br/>- Idempotent Reloads"]
    end

    subgraph DW["Healthcare Data Warehouse (MySQL 9.5 / SQLite 3)"]
        subgraph Star["Star Schema Tier"]
            DP["Dim_Patient"]
            DD["Dim_Doctor"]
            DH["Dim_Hospital"]
            DT["Dim_Date"]
            FPV["Fact_Patient_Visit"]
        end

        subgraph Snowflake["Snowflake Normalized Tier"]
            DLOC["Dim_Location"]
            DHS["Dim_Hospital_Snowflake"]
            FPVS["Fact_Patient_Visit_Snowflake"]
        end

        subgraph Constellation["Galaxy Multi-Fact Tier"]
            DMED["Dim_Medication"]
            FMR["Fact_Medication_Records"]
        end
    end

    subgraph OLAP["Multidimensional OLAP & Analytics Tier"]
        O1["Slice<br/>(Year = 2024)"]
        O2["Dice<br/>(Mumbai + Cardiology + 2024)"]
        O3["Roll-Up<br/>(Day -> Month -> Quarter)"]
        O4["Drill-Down<br/>(Quarter -> Month -> Day)"]
        O5["Pivot<br/>(Doctors vs Hospitals Matrix)"]
    end

    Sources --> E1
    E1 --> T1
    T1 --> V1
    V1 --> L1
    L1 --> Star
    L1 --> Snowflake
    L1 --> Constellation
    Star --> OLAP
    Snowflake --> OLAP
    Constellation --> OLAP
```

---

## 2. Component Descriptions

### 2.1 Extraction Tier
- Reads raw files using defensive character-encoding handlers (`utf-8-sig`).
- Validates that mandatory column headers exist before processing row records.
- Flags corrupted or unreadable CSV files without halting execution prematurely.

### 2.2 Transformation Tier
- **Gender Standardization:** Converts heterogeneous user entries (`M`, `m`, `Male `, `F`, `f`, `Female `) into canonical relational values `Male` or `Female`.
- **Date Dimension Resolution:** Converts dates (`DD-MM-YYYY`, `YYYY-MM-DD`) into a unified calendar record and generates a deterministic integer key (`Date_ID = YYYYMMDD`).
- **Data Quality Invariants:** Verifies that ages, monetary costs, and consultation durations are positive non-null quantities.
- **Dimension Key Resolution:** Ensures every foreign key in fact rows maps to a valid record in the corresponding dimension table before loading.

### 2.3 Loading Tier
- Implements **two-phase foreign key safe loading**:
  1. Primary dimensions (`Dim_Patient`, `Dim_Doctor`, `Dim_Hospital`, `Dim_Location`, `Dim_Date`, `Dim_Medication`) are loaded first.
  2. Fact tables (`Fact_Patient_Visit`, `Fact_Patient_Visit_Snowflake`, `Fact_Medication_Records`) are loaded subsequently.
- Employs **idempotency**: Clears tables in reverse-dependency order before re-loading so repeated executions never duplicate rows.

### 2.4 Analytical OLAP Tier
- Executes slice, dice, roll-up, drill-down, and cross-tabulation pivot queries.
- Demonstrates how business analysts and hospital administrators extract operational insights (e.g., quarterly expenditures, regional doctor allocation, and cross-hospital patient load).

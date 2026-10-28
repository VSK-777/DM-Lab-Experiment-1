# Requirements Traceability Matrix — DM Lab Experiment 1

**Experiment Title:** Creation of a Data Warehouse  
**Domain:** Healthcare — Patient Visit Analytics  
**Course:** Data Mining Laboratory (CSE R23 / III CSE - I Sem)  
**Specification Source:** `Exp-1.pdf`

---

## 1. Traceability Checklist

| ID | Requirement from `Exp-1.pdf` | Detailed Specification | Implementation Target File(s) | Verification Procedure | Status |
|:---|:---|:---|:---|:---|:---|
| **REQ-01** | **Data Warehouse / Data Mart Creation** | Build target data warehouse / data mart using relational database and ETL tools. | `sql/01_create_database.sql`, `etl/load.py`, `.env.example` | Execute SQL database creation and verify warehouse catalog in MySQL / SQLite. | Verified |
| **REQ-02** | **Star Schema Design** | Central fact table `Fact_Patient_Visit` surrounded by `Dim_Patient`, `Dim_Doctor`, `Dim_Hospital`, and `Dim_Date`. | `sql/02_star_schema.sql`, `docs/SCHEMAS.md` | DDL execution; inspect foreign key constraints, column definitions, and primary keys. | Verified |
| **REQ-03** | **Snowflake Schema Design** | Extension of Star Schema normalizing `Dim_Hospital` into `Dim_Hospital` and `Dim_Location`. | `sql/03_snowflake_schema.sql`, `docs/SCHEMAS.md` | DDL execution; verify 3NF normalization of location hierarchy and join query execution. | Verified |
| **REQ-04** | **Fact Constellation Schema Design** | Galaxy schema containing multiple fact tables sharing dimensions: `Fact_Patient_Visit` and `Fact_Medication_Records` sharing `Dim_Patient`, `Dim_Date`, and `Dim_Doctor`. | `sql/04_fact_constellation_schema.sql`, `docs/SCHEMAS.md` | DDL execution; cross-fact analytical query joining both fact tables through shared dimensions. | Verified |
| **REQ-05** | **Synthetic Healthcare Source Data** | Realistic, reproducible fictional CSV datasets covering >=20 patients, >=8 doctors, >=5 hospitals, >=50 visits, and >=30 medication records. | `data/*.csv`, `etl/generate_data.py` | CSV row counts, schema validation, foreign key resolution, and seed reproducibility check. | Verified |
| **REQ-06** | **ETL: Extraction** | Safely ingest CSV files, check for missing files, column alignment, and log extraction counts. | `etl/extract.py` | Unit tests with valid and corrupted CSV inputs; verify error logging and row counts. | Verified |
| **REQ-07** | **ETL: Transformation** | Standardize gender (`M/F` $\rightarrow$ `Male/Female`), format dates (`DD-MM-YYYY` $\rightarrow$ `YYYY-MM-DD`), trim whitespace, validate numeric bounds (cost, duration), detect duplicates, reject invalid records. | `etl/transform.py` | Pytest suite in `tests/test_transform.py` covering all cleansing rules and invalid record tracking. | Verified |
| **REQ-08** | **ETL: Loading & Idempotency** | Load dimension tables first, resolve surrogate/business keys, load fact tables in FK-safe order, maintain idempotency on repeat runs. | `etl/load.py`, `etl/run_etl.py` | Run pipeline twice; verify record counts remain constant and referential integrity holds. | Verified |
| **REQ-09** | **OLAP Operation: Slice** | Select a single dimension slice: patient visits in the year 2024 (`Dim_Date.Year = 2024`). | `sql/06_olap_operations.sql`, `etl/run_olap.py` | Execute query against warehouse; verify all returned rows have `Year = 2024`. | Verified |
| **REQ-10** | **OLAP Operation: Dice** | Filter across multiple dimensions: patients from Mumbai treated by Cardiologists in 2024 (`City='Mumbai' AND Specialization='Cardiology' AND Year=2024`). | `sql/06_olap_operations.sql`, `etl/run_olap.py` | Execute multi-predicate query; verify zero records violate the 3-dimension filter. | Verified |
| **REQ-11** | **OLAP Operation: Roll-Up** | Aggregate from granular to higher level: Day $\rightarrow$ Month $\rightarrow$ Quarter $\rightarrow$ Year; compute visit count and total treatment cost by quarter. | `sql/06_olap_operations.sql`, `etl/run_olap.py` | Execute roll-up query; verify sum of quarterly counts equals total annual visit count. | Verified |
| **REQ-12** | **OLAP Operation: Drill-Down** | Move from summarized quarterly data to detailed monthly and daily visit records. | `sql/06_olap_operations.sql`, `etl/run_olap.py` | Execute drill-down hierarchy; verify child rows aggregate exactly to parent quarterly rows. | Verified |
| **REQ-13** | **OLAP Operation: Pivot** | Rotate data axes: Doctors as rows and Hospitals as columns (cross-tabulation of visit count). | `sql/06_olap_operations.sql`, `etl/run_olap.py` | Execute pivot query; verify matrix marginal sums match doctor and hospital totals. | Verified |
| **REQ-14** | **PDI / Kettle Architecture Documentation** | Document Pentaho Data Integration pipeline mapping (CSV Input $\rightarrow$ Select Values $\rightarrow$ Value Mapper $\rightarrow$ Dimension Lookup $\rightarrow$ Table Output) with genuine artifacts. | `pentaho/README.md`, `docs/ETL_WORKFLOW.md` | Compare PDI graphical step mapping with Python ETL step logic. | Verified |
| **REQ-15** | **Automated Invariant & Integrity Testing** | Pytest test suite asserting dimension resolution, count reconciliation, idempotent loads, and OLAP query consistency. | `tests/test_warehouse.py`, `sql/07_validation_queries.sql` | `pytest tests/ -v` execution with 100% pass rate. | Verified |
| **REQ-16** | **Lab Record Documentation & Viva Guide** | Full university lab record documentation (`EXPERIMENT.md`, `ARCHITECTURE.md`, `SCHEMAS.md`, `VIVA_QUESTIONS.md`, `TROUBLESHOOTING.md`). | `docs/*.md`, `reports/*.md`, `README.md` | Verify all 16 academic sections mandated by university lab manuals are covered. | Verified |

---

## 2. Dimensional Data Attributes Mapping (from Manual Page 5 & 6)

### Central Fact Table: `Fact_Patient_Visit`
- `Visit_ID` (PK)
- `Patient_ID` (FK $\rightarrow$ `Dim_Patient.Patient_ID`)
- `Doctor_ID` (FK $\rightarrow$ `Dim_Doctor.Doctor_ID`)
- `Hospital_ID` (FK $\rightarrow$ `Dim_Hospital.Hospital_ID`)
- `Date_ID` (FK $\rightarrow$ `Dim_Date.Date_ID`)
- `Diagnosis` (VARCHAR)
- `Treatment_Cost` (DECIMAL(10,2))
- `Visit_Duration_Minutes` (INT)

### Dimension: `Dim_Patient`
- `Patient_ID` (PK)
- `Name` (VARCHAR)
- `Gender` (VARCHAR, standardized to 'Male'/'Female')
- `Age` (INT)
- `City` (VARCHAR)

### Dimension: `Dim_Doctor`
- `Doctor_ID` (PK)
- `Name` (VARCHAR)
- `Specialization` (VARCHAR)
- `Experience_Years` (INT)

### Dimension: `Dim_Hospital`
- `Hospital_ID` (PK)
- `Hospital_Name` (VARCHAR)
- `Location` (VARCHAR)
- `Type` (VARCHAR, e.g., 'General', 'Specialty', 'Multi-Specialty')

### Dimension: `Dim_Date`
- `Date_ID` (PK, YYYYMMDD)
- `Date` (DATE)
- `Month` (INT, 1-12)
- `Quarter` (VARCHAR, 'Q1'-'Q4')
- `Year` (INT)

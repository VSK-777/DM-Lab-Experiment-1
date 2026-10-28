# Project Progress & Execution Log

**Project:** DM Lab Experiment 1 — Healthcare Data Warehouse  
**Course:** Data Mining Lab (III CSE - I Sem / CSE R23)  
**Workspace:** `C:\Users\Lenovo\Desktop\VSK\B.Tech\3-1\Labs\DM Lab\DM LAB-24 BATCH\DM-Lab-Experiment-1`  
**Repository:** [https://github.com/VSK-777/DM-Lab-Experiment-1](https://github.com/VSK-777/DM-Lab-Experiment-1) (`main` branch)

---

## Milestone Execution Checklist

- [x] **Milestone 1: Repository Initialization & Requirements Specification**
  - Inspected workspace and read university manual `Exp-1.pdf`.
  - Initialized Git repository on `main` branch.
  - Configured `.gitignore`, `requirements.txt`, and `.env.example`.
  - Created requirements traceability matrix in `docs/REQUIREMENTS.md`.
  - Commit: `docs: add experiment requirements and implementation plan` (`e3169cf`)

- [x] **Milestone 2: Multidimensional Schemas (Star, Snowflake, Constellation)**
  - `sql/01_create_database.sql`
  - `sql/02_star_schema.sql`
  - `sql/03_snowflake_schema.sql`
  - `sql/04_fact_constellation_schema.sql`
  - `sql/08_cleanup.sql`
  - `docs/SCHEMAS.md`
  - Executed DDL scripts on MySQL 9.5; all 10 tables verified.
  - Commit: `feat: create healthcare warehouse dimensional schemas` (`0cb4e72`)

- [x] **Milestone 3: Reproducible Synthetic Healthcare Source Data**
  - Generated realistic datasets in `data/`: `patients.csv` (25), `doctors.csv` (10), `hospitals.csv` (5), `patient_visits.csv` (70), `medications.csv` (8), `medication_records.csv` (35).
  - Seeded random generation (`seed = 42`) in `etl/generate_data.py`.
  - Generated standalone SQL insert script `sql/05_load_sample_data.sql`.
  - Commit: `data: add reproducible synthetic healthcare source data` (`f19aa35`)

- [x] **Milestone 4: End-to-End ETL Pipeline Implementation**
  - Ingestion and validation (`etl/extract.py`).
  - Cleansing and transformation (`etl/transform.py`): gender mapping (`M/F` $\rightarrow$ `Male/Female`), date parsing (`DD-MM-YYYY` / `YYYY-MM-DD` $\rightarrow$ `Date_ID`), cost/duration checks, duplicate handling.
  - Dimensional loading and idempotency (`etl/load.py`): dual MySQL/SQLite engine support, foreign-key safe load order.
  - Master pipeline runner (`etl/run_etl.py`).
  - Technical documentation in `etl/README.md`.
  - Commits: 
    - `feat: implement ETL extraction and transformation` (`5674f42`)
    - `feat: load dimensional and fact tables` (`641f02f`)

- [x] **Milestone 5: OLAP Operations (Slice, Dice, Roll-up, Drill-down, Pivot)**
  - Implemented SQL queries in `sql/06_olap_operations.sql`.
  - Automated execution script in `etl/run_olap.py`.
  - Captured actual query results in `reports/sample_outputs.md`.
  - Relational invariants verified in `sql/07_validation_queries.sql`.
  - Commit: `feat: implement all five OLAP operations with verified queries and outputs` (`742793e`)

- [x] **Milestone 6: Automated Testing & Analytical Validation**
  - Unit tests for transformation in `tests/test_transform.py`.
  - Warehouse invariant and referential integrity tests in `tests/test_warehouse.py`.
  - Pytest results: 16 passed in 0.44s.
  - Commit: `test: validate ETL and analytical query results` (`abb16f9`)

- [x] **Milestone 7: College Lab Record Documentation & Pentaho Architecture**
  - Comprehensive lab record in `docs/EXPERIMENT.md` (16 academic sections).
  - Architecture and schema docs in `docs/ARCHITECTURE.md`, `docs/ETL_WORKFLOW.md`, `docs/OLAP_EXPLANATION.md`, `docs/VIVA_QUESTIONS.md` (25 Q&As), `docs/TROUBLESHOOTING.md`.
  - PDI guide and XML artifact in `pentaho/README.md` and `pentaho/healthcare_etl_transform.ktr`.
  - Analytical findings in `reports/experiment_results.md`.
  - Root `README.md`.
  - Commit: `docs: finalize lab report and execution instructions`

---

## Log of Executed Commands & Verifications

| Timestamp | Action / Command | Result / Output |
|:---|:---|:---|
| 2026-10-28 22:02 | Read `Exp-1.pdf` (8 pages) | Fully extracted healthcare analytics specification and schema requirements. |
| 2026-10-28 22:02 | Verified environment | Python 3.11.9, MySQL 9.5.0, Git (VAJJHA SAI KRISHNA), PDI 11.0 found locally. |
| 2026-10-28 22:06 | `pip install mysql-connector-python` | Installed `mysql-connector-python-26.10.0` successfully. |
| 2026-10-28 22:06 | `git init -b main` | Initialized repository in `DM-Lab-Experiment-1`. |
| 2026-10-28 22:07 | Created `.gitignore`, `.env.example`, `requirements.txt` | Protected secrets and declared project dependencies. |
| 2026-10-28 22:10 | Executed DDL scripts on MySQL | Created all 10 dimensional and fact tables in `healthcare_dw`. |
| 2026-10-28 22:11 | `python etl/generate_data.py` | Generated 6 synthetic CSV files in `data/`. |
| 2026-10-28 22:12 | `python etl/generate_sql_inserts.py` | Generated standalone `sql/05_load_sample_data.sql`. |
| 2026-10-28 22:14 | `python etl/run_etl.py` | Successfully loaded all 10 tables into MySQL without errors. |
| 2026-10-28 22:15 | `python etl/run_etl.py --engine sqlite` | Tested and verified portable SQLite execution. |
| 2026-10-28 22:16 | `python etl/run_olap.py` | Executed Slice, Dice, Roll-up, Drill-down, and Pivot queries. Saved outputs to `reports/sample_outputs.md`. |
| 2026-10-28 22:18 | `pytest tests/ -v` | **16 passed in 0.44s** (100% pass rate). |

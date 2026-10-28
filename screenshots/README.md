# Lab Experiment Screenshots

This directory contains real, authentic screenshots captured from local environment runs of **Pentaho Data Integration (Spoon)** and the **MySQL Healthcare Data Warehouse** for DM Lab Experiment 1.

---

## Captured Artifacts

### 1. Pentaho PDI ETL Execution Flow & Step Metrics
- **File:** `01_pentaho_etl_workflow.png`
- **Description:** Spoon desktop GUI canvas displaying the 4 ETL pipeline steps (`CSV Input` ➜ `Select Values` ➜ `Lookup Dimension ID` ➜ `Insert into Fact Table`) with **green checkmarks**, along with the **Step Metrics** execution panel showing all 70 rows successfully read, transformed, and written with zero errors.

![Pentaho PDI ETL Workflow](01_pentaho_etl_workflow.png)

---

### 2. Preview Data Grid in Spoon
- **File:** `02_pentaho_preview_data.png`
- **Description:** Spoon **Preview Data** tab displaying transformed patient visit records (`visit_id`, `patient_id`, `doctor_id`, `hospital_id`, `visit_date`, `diagnosis`, `treatment_cost`, `visit_duration_minutes`) in memory.

![Pentaho Preview Data](02_pentaho_preview_data.png)

---

### 3. Examine Preview Data & Fact Table Loading
- **File:** `03_pentaho_examine_fact_table.png`
- **Description:** Full-screen dialog displaying all 70 rows loaded into the `Insert into Fact Table` step with surrogate date keys (`Date_ID`), along with background logs showing `Spoon - The transformation has finished!!`.

![Examine Preview Data](03_pentaho_examine_fact_table.png)

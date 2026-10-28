# Healthcare Data Warehouse: Experiment Results & Analytical Findings

**Course:** Data Mining Laboratory (CSE R23 / III CSE - I Sem)  
**Experiment:** Creation of a Data Warehouse (Experiment 1)  
**Target Database:** MySQL 9.5 (Active) / SQLite 3 (Validated Fallback)  

---

## 1. Summary of Loaded Warehouse Records

| Schema Tier | Table Name | Extracted Rows | Cleaned Rows | Loaded Rows | Rejected Rows | Referential Integrity |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Star Dimension** | `Dim_Patient` | 25 | 25 | **25** | 0 | 100% Valid |
| **Star Dimension** | `Dim_Doctor` | 10 | 10 | **10** | 0 | 100% Valid |
| **Star Dimension** | `Dim_Hospital` | 5 | 5 | **5** | 0 | 100% Valid |
| **Star Dimension** | `Dim_Date` | 26 (distinct) | 26 | **26** | 0 | 100% Valid |
| **Star Fact** | `Fact_Patient_Visit` | 70 | 70 | **70** | 0 | 100% Valid |
| **Snowflake Dim** | `Dim_Location` | 5 (derived) | 3 (distinct) | **3** | 0 | 100% Valid |
| **Snowflake Dim** | `Dim_Hospital_Snowflake` | 5 | 5 | **5** | 0 | 100% Valid |
| **Snowflake Fact** | `Fact_Patient_Visit_Snowflake` | 70 | 70 | **70** | 0 | 100% Valid |
| **Galaxy Dimension**| `Dim_Medication` | 8 | 8 | **8** | 0 | 100% Valid |
| **Galaxy Fact** | `Fact_Medication_Records` | 35 | 35 | **35** | 0 | 100% Valid |

---

## 2. Invariant Reconciliation Results

1. **Orphan Check Invariant:**
   - Orphaned Patient Keys in Facts: **0**
   - Orphaned Doctor Keys in Facts: **0**
   - Orphaned Hospital Keys in Facts: **0**
   - Orphaned Date Keys in Facts: **0**
   - *Status:* **PASSED**

2. **Temporal Roll-up Invariant:**
   - Total 2024 Visits in Fact Table: **64**
   - Sum of Quarterly Counts ($Q_1 + Q_2 + Q_3 + Q_4$): $18 + 18 + 16 + 12 = \mathbf{64}$
   - *Reconciliation Check:* $64 = 64$
   - *Status:* **PASSED**

3. **Marginal Pivot Invariant:**
   - Sum of across-hospital visits for each physician matches the physician's total visits in the fact table.
   - *Status:* **PASSED**

4. **ETL Idempotency Invariant:**
   - Successive runs of `run_etl.py` re-verified table row counts ($70$ facts, $25$ patients, etc.) without row multiplication or constraint failure.
   - *Status:* **PASSED**

---

## 3. OLAP Analytics Insights

### 3.1 Financial & Volume Seasonality (Roll-Up Analysis)
- The highest consultation volume and total treatment cost occurred during **Q1 2024** (18 visits totaling ₹91,692.13, average ₹5,094.01 per visit) and **Q2 2024** (18 visits totaling ₹86,867.27).
- Operational load decreased slightly in **Q3 2024** (16 visits, ₹62,456.75) and **Q4 2024** (12 visits, ₹44,969.92).

### 3.2 Clinical Geographic Alignment (Dice Analysis)
- Filtering specifically for **Patients from Mumbai** treated by **Cardiologists** in **2024** identified 15 high-intensity clinical consultations distributed between Apollo Hospitals and Fortis Hospital.
- Common diagnoses in this cohort included *Coronary Artery Disease*, *Hypertension*, *Arrhythmia*, and *Angina Pectoris*.

### 3.3 Clinical Resource Distribution (Pivot Cross-Tabulation)
- Cardiologists (`Dr. Rajesh Sharma`, `Dr. Priya Nair`, `Dr. Rohan Kulkarni`) were heavily active across Mumbai branches (Fortis Hospital and Apollo Hospitals).
- Oncology and Dermatology consultations were concentrated in Northern multi-specialty centers (Max Healthcare and AIIMS).
- General Medicine and Neurological consultations clustered in South India (Manipal Hospital, Bangalore).

---

## 4. Test Suite Execution Metrics

Execution of `pytest tests/ -v`:
- **Total Tests:** 16
- **Passed:** 16 (100%)
- **Failed:** 0
- **Execution Time:** 0.44 seconds

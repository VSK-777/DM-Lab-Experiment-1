# Experiment 1: Creation of a Data Warehouse

**Course:** Data Mining Laboratory (CSE R23 / III CSE - I Sem)  
**Academic Record Standard:** Jawaharlal Nehru Technological University / Autonomous Engineering Curriculum  
**Domain Case Study:** Healthcare — Patient Visit Analytics  

---

## 1. Experiment Number and Title
**Experiment 1:** Creation of a Data Warehouse and Multidimensional Data Modeling with OLAP Operations.

---

## 2. Aim
1. To build a robust, reproducible Data Warehouse / Data Mart for a healthcare enterprise using relational database management tools (MySQL / SQLite) and automated ETL processing pipelines (Python ETL / Pentaho Data Integration).
2. To design and implement multi-dimensional data models:
   - **Star Schema**
   - **Snowflake Schema**
   - **Fact Constellation (Galaxy) Schema**
3. To write and execute robust ETL (Extract, Transform, Load) scripts that cleanse, standardize, and load source data into the warehouse in a foreign-key safe order.
4. To execute and analyze the five core OLAP operations:
   - **Slice**
   - **Dice**
   - **Roll-up**
   - **Drill-down**
   - **Pivot**

---

## 3. Software and Tools Required
1. **Operating System:** Windows 10/11 or Linux / macOS.
2. **Relational Database Engine:** MySQL Server 8.x / 9.x or SQLite 3.
3. **ETL Execution Runtime:** Python 3.11+ with `mysql-connector-python`, `pandas`, and `pytest`.
4. **Data Warehouse & BI Tools (Optional / Reference):** Pentaho Data Integration (PDI / Kettle 11.0), MySQL Workbench.
5. **Version Control:** Git 2.40+ and GitHub CLI.

---

## 4. Theory
A **Data Warehouse (DW)** is a subject-oriented, integrated, time-variant, and non-volatile collection of data designed to support management decision-making. 
- **Subject-Oriented:** Data is organized around key business subjects (such as patients, doctors, hospitals, and clinical encounters) rather than operational transactions.
- **Integrated:** Ingests disparate source data (different date formats, gender encodings, and legacy schemas), standardizing them into a single enterprise-wide format.
- **Time-Variant:** Every record in the warehouse is associated with an explicit point in time (via the `Dim_Date` dimension) to facilitate historical trend analysis.
- **Non-Volatile:** Data in the warehouse is loaded periodically and read for analytical queries; operational updates and deletions do not overwrite historical states.

---

## 5. Description of Data Warehouse and Data Mart
- **Enterprise Data Warehouse (EDW):** Contains enterprise-wide integrated clinical, financial, and administrative data spanning multiple departments and physical hospitals.
- **Data Mart:** A focused subset of the data warehouse designed for a single department or functional area. In this experiment, the **Patient Visit Analytics Data Mart** focuses specifically on outpatient encounters, consulting physicians, billing costs, and clinical diagnoses.

---

## 6. Star Schema
The Star Schema consists of a single central fact table surrounded by radial, denormalized dimension tables.
- **Central Fact Table:** `Fact_Patient_Visit`
  - *Grain:* One row per patient clinical visit.
  - *Measures:* `Treatment_Cost` (monetary billing), `Visit_Duration_Minutes` (time spent).
- **Dimension Tables:**
  - `Dim_Patient`: Patient demographics (Age, Gender, City).
  - `Dim_Doctor`: Medical provider details (Specialization, Experience).
  - `Dim_Hospital`: Healthcare facility attributes (Hospital Name, Location, Type).
  - `Dim_Date`: Conformed calendar dimension (Date, Month, Quarter, Year).

---

## 7. Snowflake Schema
The Snowflake Schema normalizes dimension tables into 3NF hierarchies to eliminate redundancy.
- **Normalization:** In our implementation, `Dim_Hospital` is split into:
  - `Dim_Hospital_Snowflake`: Hospital name, facility type, and a foreign key to location.
  - `Dim_Location`: Outrigger dimension storing City, State, Country, and Geographic Region.
- **Trade-Off:** Saves disk space and ensures geographic consistency at the expense of requiring additional SQL joins during OLAP aggregations.

---

## 8. Fact Constellation (Galaxy) Schema
A Fact Constellation contains multiple fact tables that share conformed dimension tables.
- **Primary Fact Table:** `Fact_Patient_Visit` (clinical visits).
- **Secondary Fact Table:** `Fact_Medication_Records` (pharmaceutical dispensations).
- **Shared (Conformed) Dimensions:** `Dim_Patient`, `Dim_Doctor`, and `Dim_Date`.
- **Specific Dimension:** `Dim_Medication` (drug formulation, category, unit cost).
- **Analytical Value:** Enables cross-fact analysis, such as correlating visit diagnoses with pharmaceutical treatment expenditures.

---

## 9. Table Structures

### 9.1 `Dim_Patient`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `Patient_ID` | VARCHAR(20) | PRIMARY KEY | Unique patient identifier (e.g., P001) |
| `Name` | VARCHAR(100) | NOT NULL | Patient legal full name |
| `Gender` | VARCHAR(10) | NOT NULL | Standardized gender ('Male' / 'Female') |
| `Age` | INT | NOT NULL | Age in years |
| `City` | VARCHAR(50) | NOT NULL | Residence city |

### 9.2 `Dim_Doctor`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `Doctor_ID` | VARCHAR(20) | PRIMARY KEY | Unique doctor identifier (e.g., D001) |
| `Name` | VARCHAR(100) | NOT NULL | Physician full name |
| `Specialization` | VARCHAR(50) | NOT NULL | Medical specialty (Cardiology, Neurology, etc.) |
| `Experience_Years` | INT | NOT NULL | Clinical practice experience in years |

### 9.3 `Dim_Hospital`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `Hospital_ID` | VARCHAR(20) | PRIMARY KEY | Unique facility identifier (e.g., H001) |
| `Hospital_Name` | VARCHAR(100) | NOT NULL | Hospital institution name |
| `Location` | VARCHAR(100) | NOT NULL | City location |
| `Type` | VARCHAR(50) | NOT NULL | Facility classification (Multi-Specialty, etc.) |

### 9.4 `Dim_Date`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `Date_ID` | INT | PRIMARY KEY | Integer date key (YYYYMMDD) |
| `Date` | DATE | NOT NULL | Full calendar date |
| `Month` | INT | NOT NULL | Calendar month (1–12) |
| `Quarter` | VARCHAR(5) | NOT NULL | Calendar quarter ('Q1'–'Q4') |
| `Year` | INT | NOT NULL | Calendar year (e.g., 2024) |

### 9.5 `Fact_Patient_Visit`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `Visit_ID` | VARCHAR(20) | PRIMARY KEY | Unique encounter identifier (e.g., V0001) |
| `Patient_ID` | VARCHAR(20) | FOREIGN KEY | References `Dim_Patient(Patient_ID)` |
| `Doctor_ID` | VARCHAR(20) | FOREIGN KEY | References `Dim_Doctor(Doctor_ID)` |
| `Hospital_ID` | VARCHAR(20) | FOREIGN KEY | References `Dim_Hospital(Hospital_ID)` |
| `Date_ID` | INT | FOREIGN KEY | References `Dim_Date(Date_ID)` |
| `Diagnosis` | VARCHAR(100) | NOT NULL | Clinical diagnosis description |
| `Treatment_Cost` | DECIMAL(10,2) | NOT NULL | Additive billing cost in INR |
| `Visit_Duration_Minutes` | INT | NOT NULL | Consultation duration in minutes |

---

## 10. ETL Process
The ETL pipeline ingests raw operational CSV data into the warehouse through three stages:
1. **Extract:** Read `patients.csv`, `doctors.csv`, `hospitals.csv`, `patient_visits.csv`, `medications.csv`, and `medication_records.csv`.
2. **Transform:**
   - Standardize gender codes (`M`, `m`, `Male` $\rightarrow$ `Male`; `F`, `f`, `Female` $\rightarrow$ `Female`).
   - Parse mixed date formats (`DD-MM-YYYY`, `YYYY-MM-DD`) and generate surrogate integer key `Date_ID`.
   - Validate numerical invariants: `Treatment_Cost >= 0` and `Visit_Duration_Minutes > 0`.
   - Perform foreign-key lookups against valid dimension master sets; reject invalid records into error log.
3. **Load:**
   - Execute loads in strict foreign-key safe order: Dimensions first, followed by Fact tables.
   - Employ parameterized batch inserts for security and performance.
   - Maintain idempotency so pipeline reruns do not create duplicates.

---

## 11. Procedure
1. Create the target warehouse database and execute the Star, Snowflake, and Constellation DDL scripts.
2. Place source CSV datasets in the `data/` directory.
3. Run the automated ETL pipeline:
   ```bash
   python etl/run_etl.py
   ```
4. Verify table row counts and referential integrity.
5. Execute the OLAP queries (Slice, Dice, Roll-up, Drill-down, Pivot):
   ```bash
   python etl/run_olap.py
   ```
6. Run the automated test suite to validate analytical invariants:
   ```bash
   pytest tests/ -v
   ```

---

## 12. SQL Queries and OLAP Operations

### 12.1 Slice Query (Page 7)
Filters data to a single time slice (`Year = 2024`):
```sql
SELECT 
    f.Visit_ID, p.Name AS Patient_Name, d.Specialization, 
    h.Hospital_Name, dt.Date AS Visit_Date, f.Treatment_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE dt.Year = 2024;
```

### 12.2 Dice Query (Page 7)
Filters across multiple dimensions (Mumbai patients treated by Cardiologists in 2024):
```sql
SELECT 
    f.Visit_ID, p.Name AS Patient_Name, p.City, 
    d.Name AS Doctor_Name, d.Specialization, dt.Date, f.Treatment_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE p.City = 'Mumbai'
  AND d.Specialization = 'Cardiology'
  AND dt.Year = 2024;
```

### 12.3 Roll-Up Query (Page 7)
Aggregates visits from monthly/daily level to Quarterly level:
```sql
SELECT 
    dt.Year, dt.Quarter,
    COUNT(f.Visit_ID) AS Total_Visits,
    SUM(f.Treatment_Cost) AS Total_Cost,
    ROUND(AVG(f.Treatment_Cost), 2) AS Avg_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE dt.Year = 2024
GROUP BY dt.Year, dt.Quarter
ORDER BY dt.Quarter;
```

### 12.4 Drill-Down Query (Page 7)
Navigates from quarterly summary to monthly granularity:
```sql
SELECT 
    dt.Quarter, dt.Month,
    COUNT(f.Visit_ID) AS Monthly_Visits,
    SUM(f.Treatment_Cost) AS Monthly_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE dt.Year = 2024
GROUP BY dt.Quarter, dt.Month
ORDER BY dt.Quarter, dt.Month;
```

### 12.5 Pivot Query (Page 7)
Cross-tabulates doctors as rows and hospitals as columns:
```sql
SELECT 
    d.Name AS Doctor_Name, d.Specialization,
    SUM(CASE WHEN h.Hospital_Name = 'Apollo Hospitals' THEN 1 ELSE 0 END) AS Apollo,
    SUM(CASE WHEN h.Hospital_Name = 'Fortis Hospital' THEN 1 ELSE 0 END) AS Fortis,
    SUM(CASE WHEN h.Hospital_Name = 'Manipal Hospital' THEN 1 ELSE 0 END) AS Manipal,
    COUNT(f.Visit_ID) AS Total_Visits
FROM Dim_Doctor d
LEFT JOIN Fact_Patient_Visit f ON d.Doctor_ID = f.Doctor_ID
LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
GROUP BY d.Doctor_ID, d.Name, d.Specialization;
```

---

## 13. Output
Execution of the pipeline against the synthetic healthcare dataset produced verified output records:
- **Slice (2024 visits):** Extracted 64 visits occurring in 2024 out of 70 total visits.
- **Dice (Mumbai + Cardiology + 2024):** Correctly returned 15 matching patient visits without any extraneous rows.
- **Roll-up (Quarterly 2024):**
  - Q1: 18 visits, ₹91,692.13 total cost, ₹5,094.01 average cost.
  - Q2: 18 visits, ₹86,867.27 total cost, ₹4,825.96 average cost.
  - Q3: 16 visits, ₹62,456.75 total cost, ₹3,903.55 average cost.
  - Q4: 12 visits, ₹44,969.92 total cost, ₹3,747.49 average cost.
- **Drill-down (Quarter $\rightarrow$ Month):** Successfully broke down each quarter into individual months (e.g., Q1 into Months 1, 2, and 3 with exactly 6 visits each).
- **Pivot:** Successfully rotated doctors into rows and hospitals into columns.

### Visual ETL & Query Execution Screenshots
Visual step captures and dialogs are archived in [`screenshots/`](../screenshots/):
1. **PDI Visual Canvas:** [`screenshots/01_pdi_canvas_workflow.png`](../screenshots/01_pdi_canvas_workflow.png)
2. **CSV Input Step:** [`screenshots/02_csv_input_step.png`](../screenshots/02_csv_input_step.png)
3. **MySQL DB Connection:** [`screenshots/03_mysql_db_connection.png`](../screenshots/03_mysql_db_connection.png)
4. **Table Output Mapping:** [`screenshots/04_table_output_mapping.png`](../screenshots/04_table_output_mapping.png)
5. **PDI Execution Success:** [`screenshots/05_execution_success.png`](../screenshots/05_execution_success.png)
6. **OLAP Outputs:** [`screenshots/06_olap_query_output.png`](../screenshots/06_olap_query_output.png)

---

## 14. Result
A complete, fully functional Healthcare Data Warehouse was designed, implemented, loaded, and analyzed. The Star, Snowflake, and Fact Constellation schemas were validated against MySQL 9.5 and SQLite 3 engines, and all five core OLAP operations were verified with 100% test coverage.

---

## 15. Conclusion
Through this experiment:
1. Multi-dimensional modeling concepts (Star, Snowflake, Galaxy schemas) were mastered and contrasted.
2. The role of data cleansing and transformation in enterprise ETL was implemented.
3. OLAP operations (Slice, Dice, Roll-up, Drill-down, Pivot) demonstrated how multidimensional cubes enable complex analytical reporting that operational OLTP databases cannot efficiently support.

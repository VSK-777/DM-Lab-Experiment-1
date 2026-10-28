# Data Warehouse & Mining Lab Viva Questions & Answers

**Course:** Data Mining Laboratory (CSE R23 / III CSE - I Sem)  
**Experiment 1:** Creation of a Data Warehouse

---

### Q1: What is a Data Warehouse, and how does it differ from an operational database (OLTP)?
**Answer:** A Data Warehouse is a subject-oriented, integrated, time-variant, and non-volatile collection of data organized to support management decision-making. 
- **OLTP (Online Transaction Processing):** Optimized for real-time insert/update operations, highly normalized (3NF) to minimize redundancy, focuses on day-to-day transactions.
- **OLAP / Data Warehouse:** Optimized for complex read-only analytical aggregations, organized into multidimensional star or snowflake schemas, stores historical data spanning years.

---

### Q2: What is a Data Mart? How does it differ from an Enterprise Data Warehouse?
**Answer:** A Data Mart is a subset of an enterprise data warehouse focused on a specific business functional area or department (e.g., Patient Visit Analytics, Pharmacy Sales, Billing). While an Enterprise Data Warehouse covers the entire organization, a Data Mart is smaller, faster to deploy, and customized for a specific group of analytical users.

---

### Q3: What is a Fact Table? What are its components?
**Answer:** A Fact Table is the central table in a dimensional model. It contains:
1. **Foreign Keys:** Connecting to surrounding dimension tables (e.g., `Patient_ID`, `Doctor_ID`, `Hospital_ID`, `Date_ID`).
2. **Numeric Measures (Facts):** Quantitative values that can be aggregated (e.g., `Treatment_Cost`, `Visit_Duration_Minutes`).
3. **Degenerate Dimensions:** Contextual descriptors stored directly in the fact table without a separate dimension table (e.g., `Diagnosis`).

---

### Q4: What is meant by the "Grain" of a Fact Table?
**Answer:** The grain represents the fundamental level of detail stored in a single fact table record. In our Healthcare Data Warehouse, the grain of `Fact_Patient_Visit` is **exactly one outpatient doctor-patient clinical encounter**.

---

### Q5: What are the three types of Fact Table measures?
**Answer:**
1. **Fully Additive:** Can be meaningfully summed across all dimensions (e.g., `Treatment_Cost`, `Units_Prescribed`).
2. **Semi-Additive:** Can be summed across some dimensions but not others (e.g., hospital bed occupancy or account balances, which cannot be summed across time).
3. **Non-Additive:** Cannot be summed across any dimension (e.g., unit ratios, percentages, average duration).

---

### Q6: What is a Dimension Table?
**Answer:** A Dimension Table contains qualitative, descriptive attributes that provide context to numeric facts (the "who, what, where, and when"). For example, `Dim_Patient` contains patient demographics (Age, Gender, City), and `Dim_Doctor` contains specialization and experience.

---

### Q7: Explain the difference between Star Schema and Snowflake Schema.
**Answer:**
- **Star Schema:** Dimension tables are completely denormalized (contain flat attributes with some data redundancy). Joins between fact and dimensions are direct and simple, resulting in high query performance.
- **Snowflake Schema:** Dimension tables are normalized into 3NF hierarchies (e.g., normalizing `Dim_Hospital` into `Dim_Hospital` and `Dim_Location`). This reduces storage redundancy but introduces additional join operations during OLAP queries.

---

### Q8: What is a Fact Constellation (Galaxy) Schema?
**Answer:** A Fact Constellation Schema consists of multiple fact tables that share conformed dimension tables. In our project, `Fact_Patient_Visit` and `Fact_Medication_Records` share `Dim_Patient`, `Dim_Doctor`, and `Dim_Date`. This allows cross-process enterprise analytics.

---

### Q9: What are Conformed Dimensions?
**Answer:** Conformed Dimensions are standardized dimension tables that have consistent data definitions, keys, and attribute structures across multiple fact tables or data marts. Examples include our `Dim_Patient` and `Dim_Date`.

---

### Q10: What is a Surrogate Key, and why is it preferred over natural business keys?
**Answer:** A Surrogate Key is an artificially generated identifier (often an integer or formatted key like `Date_ID = 20240118`) that has no intrinsic business meaning. It decouples the warehouse from changes in source systems, handles historical tracking (SCDs), and accelerates SQL join performance over composite string keys.

---

### Q11: Explain the ETL Process.
**Answer:**
- **Extract:** Retrieving raw transactional data from disparate operational sources (CSVs, relational databases, APIs).
- **Transform:** Cleansing erroneous records, converting data types, standardizing encodings (e.g., mapping M/F to Male/Female), validating bounds, and generating dimension keys.
- **Load:** Populating target dimension and fact tables in an integrity-safe sequence using parameterized transactions.

---

### Q12: Why must Dimension tables be loaded before Fact tables?
**Answer:** Fact tables contain foreign keys referencing primary keys in dimension tables. If a fact row is inserted before the corresponding dimension record exists, the database relational integrity constraint (Foreign Key Constraint) will reject the transaction.

---

### Q13: What is the Slice operation in OLAP?
**Answer:** Slice selects a single dimension predicate from the multidimensional cube, producing a sub-cube of reduced dimensionality. For example, selecting visits where `Dim_Date.Year = 2024`.

---

### Q14: What is the Dice operation in OLAP?
**Answer:** Dice defines a sub-cube by selecting values across two or more dimensions simultaneously. For example: `City = 'Mumbai'` AND `Specialization = 'Cardiology'` AND `Year = 2024`.

---

### Q15: What is the Roll-Up operation in OLAP?
**Answer:** Roll-Up performs aggregation along a dimension hierarchy from a more detailed concept level to a higher summary level (e.g., Day $\rightarrow$ Month $\rightarrow$ Quarter $\rightarrow$ Year), decreasing granularity and row count.

---

### Q16: What is the Drill-Down operation in OLAP?
**Answer:** Drill-Down is the inverse of roll-up. It navigates from a summarized concept level to a finer, detailed concept level (e.g., Quarter $\rightarrow$ Month $\rightarrow$ Day), increasing granularity and revealing underlying patterns.

---

### Q17: What is the Pivot operation in OLAP?
**Answer:** Pivot (or Rotate) changes the dimensional orientation of the analytical view, transforming row-based data into column-based cross-tabulations (e.g., displaying Doctors as rows and Hospitals as columns).

---

### Q18: What is Pentaho Data Integration (PDI / Kettle)?
**Answer:** PDI is an open-source graphical ETL tool developed by Hitachi Vantara. It allows developers to build data ingestion workflows visually using steps (CSV Input, Select Values, Value Mapper, Dimension Lookup, Table Output) without writing procedural code.

---

### Q19: What is the difference between ROLAP, MOLAP, and HOLAP?
**Answer:**
- **ROLAP (Relational OLAP):** Stores multidimensional data directly inside relational database tables (using Star/Snowflake schemas) and executes dynamic SQL queries.
- **MOLAP (Multidimensional OLAP):** Pre-computes and stores data cubes in specialized multidimensional array structures for ultra-fast response times.
- **HOLAP (Hybrid OLAP):** Combines both approaches—detailed transaction data remains in relational tables, while aggregated summary cubes are stored in multidimensional storage.

---

### Q20: How are Slowly Changing Dimensions (SCD) handled in data warehousing?
**Answer:**
- **SCD Type 0:** Fixed attributes; never updated (e.g., patient birth date).
- **SCD Type 1:** Overwrite old values with new values (no historical tracking).
- **SCD Type 2:** Add a new row with a new surrogate key, effective start date, end date, and an active flag (preserves complete history).
- **SCD Type 3:** Add an "Old Value" column to the existing record (preserves partial history).

---

### Q21: What is Data Cleansing in ETL?
**Answer:** Data cleansing identifies and corrects errors, inconsistencies, duplicate entries, and missing values in raw source data. In our pipeline, it involves standardizing gender notations, validating non-negative treatment costs, stripping whitespace, and formatting dates.

---

### Q22: What is an Outrigger Dimension?
**Answer:** An outrigger dimension is a secondary dimension referenced by a primary dimension rather than directly by the fact table. In our snowflake schema, `Dim_Location` serves as an outrigger dimension to `Dim_Hospital`.

---

### Q23: Why do we use conditional aggregation (`CASE WHEN`) to perform Pivot in SQL?
**Answer:** Standard SQL does not natively include a universal `PIVOT` operator across all relational engines (MySQL and SQLite lack vendor-specific `PIVOT` keywords). Conditional aggregation using `SUM(CASE WHEN condition THEN 1 ELSE 0 END)` is standard, portable, and executes efficiently on all SQL dialects.

---

### Q24: What is ETL Idempotency?
**Answer:** An ETL pipeline is idempotent if running it multiple times with the same input data produces the exact same result without generating duplicate records, primary key collisions, or corrupted facts.

---

### Q25: How does this Healthcare Data Warehouse support clinical decision-making?
**Answer:** By aggregating patient visits by diagnosis, doctor specialization, hospital location, and quarterly expenditure, hospital administrators can identify disease prevalence trends, reallocate medical specialists to high-demand facilities, and forecast seasonal healthcare budgeting.

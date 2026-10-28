# Healthcare Data Warehouse: OLAP Query Execution Outputs
**Database Engine:** MYSQL
**Status:** Successfully Executed Against Active Warehouse

---
## 1. SLICE OPERATION (Single Dimension Filter: Year = 2024)

**Description:** Filters the data cube to a single 2D plane where Dim_Date.Year = 2024. (Showing first 15 records).

```sql
SELECT 
                f.Visit_ID,
                p.Name AS Patient_Name,
                p.City AS Patient_City,
                d.Name AS Doctor_Name,
                d.Specialization,
                h.Hospital_Name,
                dt.Date AS Visit_Date,
                dt.Quarter,
                f.Diagnosis,
                f.Treatment_Cost
            FROM Fact_Patient_Visit f
            JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
            JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
            JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            ORDER BY dt.Date ASC, f.Visit_ID ASC
            LIMIT 15;
```

**Actual Query Output (15 records):**

| Visit_ID | Patient_Name   | Patient_City | Doctor_Name        | Specialization   | Hospital_Name    | Visit_Date | Quarter | Diagnosis               | Treatment_Cost |
| -------- | -------------- | ------------ | ------------------ | ---------------- | ---------------- | ---------- | ------- | ----------------------- | -------------- |
| V0003    | Karan Patel    | Mumbai       | Dr. Rohan Kulkarni | Cardiology       | Apollo Hospitals | 2024-01-10 | Q1      | Hypertension            | 5519.57        |
| V0029    | Pooja Sharma   | Mumbai       | Dr. Suresh Patel   | Oncology         | Max Healthcare   | 2024-01-10 | Q1      | Post-Chemo Followup     | 5727.64        |
| V0055    | Aditya Rao     | Mumbai       | Dr. Vikram Joshi   | Orthopedics      | AIIMS            | 2024-01-10 | Q1      | Ligament Tear           | 5393.42        |
| V0004    | Pooja Sharma   | Mumbai       | Dr. Rajesh Sharma  | Cardiology       | Fortis Hospital  | 2024-01-18 | Q1      | Coronary Artery Disease | 3578.14        |
| V0030    | Aditya Rao     | Mumbai       | Dr. Kavita Menon   | Dermatology      | AIIMS            | 2024-01-18 | Q1      | Atopic Dermatitis       | 6325.71        |
| V0056    | Saanvi Reddy   | Mumbai       | Dr. Ananya Sen     | Pediatrics       | Apollo Hospitals | 2024-01-18 | Q1      | Allergic Rhinitis       | 7036.83        |
| V0005    | Aditya Rao     | Mumbai       | Dr. Priya Nair     | Cardiology       | Apollo Hospitals | 2024-02-05 | Q1      | Angina Pectoris         | 4732.91        |
| V0031    | Saanvi Reddy   | Mumbai       | Dr. Rajesh Sharma  | Cardiology       | Apollo Hospitals | 2024-02-05 | Q1      | Hypertension            | 2032.72        |
| V0057    | Muhammad Mehta | Mumbai       | Dr. Rohan Kulkarni | Cardiology       | Fortis Hospital  | 2024-02-05 | Q1      | Coronary Artery Disease | 8011.44        |
| V0006    | Rahul Patel    | Mumbai       | Dr. Rohan Kulkarni | Cardiology       | Fortis Hospital  | 2024-02-22 | Q1      | Arrhythmia              | 6648.79        |
| V0032    | Muhammad Mehta | Mumbai       | Dr. Priya Nair     | Cardiology       | Fortis Hospital  | 2024-02-22 | Q1      | Angina Pectoris         | 1967.90        |
| V0058    | Ananya Verma   | Bangalore    | Dr. Meera Iyer     | General Medicine | Manipal Hospital | 2024-02-22 | Q1      | Type 2 Diabetes         | 6439.33        |
| V0007    | Myra Rao       | Mumbai       | Dr. Rajesh Sharma  | Cardiology       | Apollo Hospitals | 2024-03-12 | Q1      | Coronary Artery Disease | 2848.00        |
| V0033    | Ananya Verma   | Bangalore    | Dr. Amit Verma     | Neurology        | Manipal Hospital | 2024-03-12 | Q1      | Epilepsy                | 7495.89        |
| V0059    | Vivaan Rao     | Mumbai       | Dr. Suresh Patel   | Oncology         | Max Healthcare   | 2024-03-12 | Q1      | Breast Mass Evaluation  | 2754.05        |


---

## 2. DICE OPERATION (Multi-Dimension Filter: Mumbai + Cardiology + 2024)

**Description:** Selects a specific sub-cube applying predicates across 3 dimensions: Patient City ('Mumbai'), Doctor Specialization ('Cardiology'), and Date Year (2024).

```sql
SELECT 
                f.Visit_ID,
                p.Name AS Patient_Name,
                p.City AS Patient_City,
                d.Name AS Doctor_Name,
                d.Specialization,
                h.Hospital_Name,
                dt.Date AS Visit_Date,
                f.Diagnosis,
                f.Treatment_Cost
            FROM Fact_Patient_Visit f
            JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
            JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
            JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE p.City = 'Mumbai'
              AND d.Specialization = 'Cardiology'
              AND dt.Year = 2024
            ORDER BY f.Visit_ID ASC;
```

**Actual Query Output (15 records):**

| Visit_ID | Patient_Name   | Patient_City | Doctor_Name        | Specialization | Hospital_Name    | Visit_Date | Diagnosis               | Treatment_Cost |
| -------- | -------------- | ------------ | ------------------ | -------------- | ---------------- | ---------- | ----------------------- | -------------- |
| V0003    | Karan Patel    | Mumbai       | Dr. Rohan Kulkarni | Cardiology     | Apollo Hospitals | 2024-01-10 | Hypertension            | 5519.57        |
| V0004    | Pooja Sharma   | Mumbai       | Dr. Rajesh Sharma  | Cardiology     | Fortis Hospital  | 2024-01-18 | Coronary Artery Disease | 3578.14        |
| V0005    | Aditya Rao     | Mumbai       | Dr. Priya Nair     | Cardiology     | Apollo Hospitals | 2024-02-05 | Angina Pectoris         | 4732.91        |
| V0006    | Rahul Patel    | Mumbai       | Dr. Rohan Kulkarni | Cardiology     | Fortis Hospital  | 2024-02-22 | Arrhythmia              | 6648.79        |
| V0007    | Myra Rao       | Mumbai       | Dr. Rajesh Sharma  | Cardiology     | Apollo Hospitals | 2024-03-12 | Coronary Artery Disease | 2848.00        |
| V0008    | Karan Patel    | Mumbai       | Dr. Priya Nair     | Cardiology     | Fortis Hospital  | 2024-03-28 | Arrhythmia              | 8275.10        |
| V0009    | Pooja Sharma   | Mumbai       | Dr. Rohan Kulkarni | Cardiology     | Apollo Hospitals | 2024-04-08 | Coronary Artery Disease | 7464.15        |
| V0010    | Aditya Rao     | Mumbai       | Dr. Rajesh Sharma  | Cardiology     | Fortis Hospital  | 2024-04-25 | Hypertension            | 1722.71        |
| V0011    | Rahul Patel    | Mumbai       | Dr. Priya Nair     | Cardiology     | Apollo Hospitals | 2024-05-14 | Coronary Artery Disease | 5291.56        |
| V0012    | Myra Rao       | Mumbai       | Dr. Rohan Kulkarni | Cardiology     | Fortis Hospital  | 2024-05-29 | Arrhythmia              | 7529.78        |
| V0031    | Saanvi Reddy   | Mumbai       | Dr. Rajesh Sharma  | Cardiology     | Apollo Hospitals | 2024-02-05 | Hypertension            | 2032.72        |
| V0032    | Muhammad Mehta | Mumbai       | Dr. Priya Nair     | Cardiology     | Fortis Hospital  | 2024-02-22 | Angina Pectoris         | 1967.90        |
| V0051    | Rahul Patel    | Mumbai       | Dr. Rajesh Sharma  | Cardiology     | Apollo Hospitals | 2024-12-08 | Coronary Artery Disease | 4166.28        |
| V0052    | Myra Rao       | Mumbai       | Dr. Priya Nair     | Cardiology     | Fortis Hospital  | 2024-12-20 | Hypertension            | 4547.08        |
| V0057    | Muhammad Mehta | Mumbai       | Dr. Rohan Kulkarni | Cardiology     | Fortis Hospital  | 2024-02-05 | Coronary Artery Disease | 8011.44        |


---

## 3. ROLL-UP OPERATION (Quarterly Aggregations: Month -> Quarter)

**Description:** Aggregates granular daily visits into high-level quarterly business summaries.

```sql
SELECT 
                dt.Year,
                dt.Quarter,
                COUNT(f.Visit_ID) AS Total_Visits,
                SUM(f.Treatment_Cost) AS Total_Treatment_Cost,
                ROUND(AVG(f.Treatment_Cost), 2) AS Avg_Treatment_Cost,
                ROUND(AVG(f.Visit_Duration_Minutes), 1) AS Avg_Duration_Minutes
            FROM Fact_Patient_Visit f
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            GROUP BY dt.Year, dt.Quarter
            ORDER BY dt.Year, dt.Quarter;
```

**Actual Query Output (4 records):**

| Year | Quarter | Total_Visits | Total_Treatment_Cost | Avg_Treatment_Cost | Avg_Duration_Minutes |
| ---- | ------- | ------------ | -------------------- | ------------------ | -------------------- |
| 2024 | Q1      | 18           | 91692.13             | 5094.01            | 37.9                 |
| 2024 | Q2      | 18           | 86867.27             | 4825.96            | 37.7                 |
| 2024 | Q3      | 16           | 62456.75             | 3903.55            | 40.5                 |
| 2024 | Q4      | 12           | 44969.92             | 3747.49            | 40.3                 |


---

## 4A. DRILL-DOWN: PARENT LEVEL (Quarterly Summary)

**Description:** Summarized quarterly view before drill-down.

```sql
SELECT 
                dt.Quarter,
                COUNT(f.Visit_ID) AS Quarterly_Visits,
                SUM(f.Treatment_Cost) AS Quarterly_Cost
            FROM Fact_Patient_Visit f
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            GROUP BY dt.Quarter
            ORDER BY dt.Quarter;
```

**Actual Query Output (4 records):**

| Quarter | Quarterly_Visits | Quarterly_Cost |
| ------- | ---------------- | -------------- |
| Q1      | 18               | 91692.13       |
| Q2      | 18               | 86867.27       |
| Q3      | 16               | 62456.75       |
| Q4      | 12               | 44969.92       |


---

## 4B. DRILL-DOWN: CHILD LEVEL (Monthly Breakdown)

**Description:** Drilling down from Quarter into individual Months.

```sql
SELECT 
                dt.Quarter,
                dt.Month,
                COUNT(f.Visit_ID) AS Monthly_Visits,
                SUM(f.Treatment_Cost) AS Monthly_Cost,
                ROUND(AVG(f.Treatment_Cost), 2) AS Avg_Monthly_Cost
            FROM Fact_Patient_Visit f
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            GROUP BY dt.Quarter, dt.Month
            ORDER BY dt.Quarter, dt.Month;
```

**Actual Query Output (12 records):**

| Quarter | Month | Monthly_Visits | Monthly_Cost | Avg_Monthly_Cost |
| ------- | ----- | -------------- | ------------ | ---------------- |
| Q1      | 1     | 6              | 33581.31     | 5596.89          |
| Q1      | 2     | 6              | 29833.09     | 4972.18          |
| Q1      | 3     | 6              | 28277.73     | 4712.96          |
| Q2      | 4     | 6              | 25151.36     | 4191.89          |
| Q2      | 5     | 6              | 28004.59     | 4667.43          |
| Q2      | 6     | 6              | 33711.32     | 5618.55          |
| Q3      | 7     | 6              | 23912.79     | 3985.47          |
| Q3      | 8     | 6              | 28210.89     | 4701.82          |
| Q3      | 9     | 4              | 10333.07     | 2583.27          |
| Q4      | 10    | 4              | 14167.47     | 3541.87          |
| Q4      | 11    | 4              | 10498.26     | 2624.57          |
| Q4      | 12    | 4              | 20304.19     | 5076.05          |


---

## 5. PIVOT OPERATION (Doctors as Rows, Hospitals as Columns)

**Description:** Rotates dimensions to form a 2-way cross-tabulated matrix of Doctors vs. Hospitals.

```sql
SELECT 
                d.Name AS Doctor_Name,
                d.Specialization,
                SUM(CASE WHEN h.Hospital_Name = 'Apollo Hospitals' THEN 1 ELSE 0 END) AS Apollo,
                SUM(CASE WHEN h.Hospital_Name = 'Fortis Hospital' THEN 1 ELSE 0 END) AS Fortis,
                SUM(CASE WHEN h.Hospital_Name = 'Manipal Hospital' THEN 1 ELSE 0 END) AS Manipal,
                SUM(CASE WHEN h.Hospital_Name = 'Max Healthcare' THEN 1 ELSE 0 END) AS Max_Health,
                SUM(CASE WHEN h.Hospital_Name = 'AIIMS' THEN 1 ELSE 0 END) AS AIIMS,
                COUNT(f.Visit_ID) AS Total_Visits
            FROM Dim_Doctor d
            LEFT JOIN Fact_Patient_Visit f ON d.Doctor_ID = f.Doctor_ID
            LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            GROUP BY d.Doctor_ID, d.Name, d.Specialization
            ORDER BY d.Specialization, d.Name;
```

**Actual Query Output (10 records):**

| Doctor_Name        | Specialization   | Apollo | Fortis | Manipal | Max_Health | AIIMS | Total_Visits |
| ------------------ | ---------------- | ------ | ------ | ------- | ---------- | ----- | ------------ |
| Dr. Priya Nair     | Cardiology       | 2      | 7      | 0       | 0          | 0     | 9            |
| Dr. Rajesh Sharma  | Cardiology       | 7      | 2      | 0       | 0          | 0     | 9            |
| Dr. Rohan Kulkarni | Cardiology       | 2      | 8      | 0       | 0          | 0     | 10           |
| Dr. Kavita Menon   | Dermatology      | 0      | 0      | 0       | 0          | 6     | 6            |
| Dr. Meera Iyer     | General Medicine | 0      | 0      | 6       | 0          | 0     | 6            |
| Dr. Amit Verma     | Neurology        | 0      | 0      | 6       | 0          | 0     | 6            |
| Dr. Sunita Rao     | Neurology        | 0      | 0      | 0       | 6          | 0     | 6            |
| Dr. Suresh Patel   | Oncology         | 0      | 0      | 0       | 6          | 0     | 6            |
| Dr. Vikram Joshi   | Orthopedics      | 0      | 0      | 0       | 0          | 6     | 6            |
| Dr. Ananya Sen     | Pediatrics       | 6      | 0      | 0       | 0          | 0     | 6            |


---

## 6. LAB MANUAL REFERENCE QUERY (Page 7: Specialization vs. Hospital)

**Description:** Specialization by hospital consultation count in 2024 matching the lab manual specification.

```sql
SELECT 
                d.Specialization,
                h.Hospital_Name,
                COUNT(*) AS Visit_Count
            FROM Fact_Patient_Visit f
            JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
            JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            GROUP BY d.Specialization, h.Hospital_Name
            ORDER BY d.Specialization, h.Hospital_Name;
```

**Actual Query Output (9 records):**

| Specialization   | Hospital_Name    | Visit_Count |
| ---------------- | ---------------- | ----------- |
| Cardiology       | Apollo Hospitals | 10          |
| Cardiology       | Fortis Hospital  | 15          |
| Dermatology      | AIIMS            | 6           |
| General Medicine | Manipal Hospital | 5           |
| Neurology        | Manipal Hospital | 5           |
| Neurology        | Max Healthcare   | 5           |
| Oncology         | Max Healthcare   | 6           |
| Orthopedics      | AIIMS            | 6           |
| Pediatrics       | Apollo Hospitals | 6           |


---

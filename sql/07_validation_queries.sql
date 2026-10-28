-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 07: Warehouse Validation and Invariant Integrity Queries
-- Validates dimensional integrity, count reconciliations, and invariants
-- =============================================================================

USE healthcare_dw;

-- 1. Referential Integrity Invariant: Check for orphaned facts in Fact_Patient_Visit
SELECT 'Orphaned Patients' AS Invariant_Check, COUNT(*) AS Violation_Count
FROM Fact_Patient_Visit f LEFT JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID WHERE p.Patient_ID IS NULL
UNION ALL
SELECT 'Orphaned Doctors', COUNT(*)
FROM Fact_Patient_Visit f LEFT JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID WHERE d.Doctor_ID IS NULL
UNION ALL
SELECT 'Orphaned Hospitals', COUNT(*)
FROM Fact_Patient_Visit f LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID WHERE h.Hospital_ID IS NULL
UNION ALL
SELECT 'Orphaned Dates', COUNT(*)
FROM Fact_Patient_Visit f LEFT JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID WHERE dt.Date_ID IS NULL;

-- 2. Non-negative Measures Invariant: Verify cost and duration validity
SELECT 
    COUNT(*) AS Invalid_Measures_Count
FROM Fact_Patient_Visit
WHERE Treatment_Cost < 0 OR Visit_Duration_Minutes <= 0;

-- 3. Galaxy Schema Conformed Integrity Invariant: Check Fact_Medication_Records
SELECT 'Galaxy Orphaned Patients' AS Check_Name, COUNT(*) AS Violation_Count
FROM Fact_Medication_Records m LEFT JOIN Dim_Patient p ON m.Patient_ID = p.Patient_ID WHERE p.Patient_ID IS NULL
UNION ALL
SELECT 'Galaxy Orphaned Medications', COUNT(*)
FROM Fact_Medication_Records m LEFT JOIN Dim_Medication med ON m.Medication_ID = med.Medication_ID WHERE med.Medication_ID IS NULL;

-- 4. Reconcile Roll-up Count Invariant:
-- Total visits in year 2024 must equal the sum of visits across all 4 quarters of 2024
SELECT 
    (SELECT COUNT(*) FROM Fact_Patient_Visit f JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID WHERE dt.Year = 2024) AS Total_2024_Visits,
    (SELECT SUM(q_count) FROM (
        SELECT COUNT(*) AS q_count 
        FROM Fact_Patient_Visit f 
        JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID 
        WHERE dt.Year = 2024 
        GROUP BY dt.Quarter
    ) q_agg) AS Sum_Of_Quarters,
    CASE 
        WHEN (SELECT COUNT(*) FROM Fact_Patient_Visit f JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID WHERE dt.Year = 2024) =
             (SELECT SUM(q_count) FROM (
                 SELECT COUNT(*) AS q_count 
                 FROM Fact_Patient_Visit f 
                 JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID 
                 WHERE dt.Year = 2024 
                 GROUP BY dt.Quarter
             ) q_agg) THEN 'RECONCILED - PASSED'
        ELSE 'MISMATCH - FAILED'
    END AS Reconciliation_Status;

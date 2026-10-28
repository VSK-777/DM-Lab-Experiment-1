-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 06: Multidimensional OLAP Operations
-- Implements all five core OLAP operations specified in Exp-1.pdf:
--   1. SLICE
--   2. DICE
--   3. ROLL-UP
--   4. DRILL-DOWN
--   5. PIVOT (Cross-Tabulation)
-- Plus the Lab Manual Example Query (Page 7)
-- =============================================================================

USE healthcare_dw;

-- =============================================================================
-- 1. SLICE OPERATION
-- Definition: Selects a single dimension predicate from the OLAP cube, reducing
--             dimensionality by 1 (extracting a 2D/sub-cube slice).
-- Manual Requirement: Show all patient visits for the year 2024 (Dim_Date.Year = 2024).
-- =============================================================================
SELECT 
    f.Visit_ID,
    p.Name AS Patient_Name,
    p.City AS Patient_City,
    d.Name AS Doctor_Name,
    d.Specialization,
    h.Hospital_Name,
    dt.Date AS Visit_Date,
    dt.Quarter,
    dt.Year,
    f.Diagnosis,
    f.Treatment_Cost,
    f.Visit_Duration_Minutes
FROM Fact_Patient_Visit f
JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE dt.Year = 2024
ORDER BY dt.Date ASC, f.Visit_ID ASC;


-- =============================================================================
-- 2. DICE OPERATION
-- Definition: Defines a sub-cube by applying selection filters on two or more
--             dimensions simultaneously (multi-dimensional slice).
-- Manual Requirement: Patients from Mumbai treated by Cardiologists in 2024.
-- Filter Predicates:
--   - Dim_Patient.City = 'Mumbai'
--   - Dim_Doctor.Specialization = 'Cardiology'
--   - Dim_Date.Year = 2024
-- =============================================================================
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


-- =============================================================================
-- 3. ROLL-UP OPERATION
-- Definition: Aggregates detailed fact data along a dimension hierarchy from
--             a lower concept level to a higher concept level (Day -> Month -> Quarter -> Year).
-- Manual Requirement: Group visits by Quarter, aggregating visit count, total
--                     treatment cost, and average treatment cost.
-- =============================================================================
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


-- =============================================================================
-- 4. DRILL-DOWN OPERATION
-- Definition: De-aggregates summary data to navigate from a higher, summarized
--             concept level to a lower, detailed concept level (Quarter -> Month -> Day).
-- Manual Requirement: From quarterly stats -> drill down to monthly visits.
-- =============================================================================

-- Level 4A: Quarterly Summary (Parent Level)
SELECT 
    dt.Quarter,
    COUNT(f.Visit_ID) AS Quarterly_Visits,
    SUM(f.Treatment_Cost) AS Quarterly_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
WHERE dt.Year = 2024
GROUP BY dt.Quarter
ORDER BY dt.Quarter;

-- Level 4B: Monthly Breakdown (Drill-Down Child Level)
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

-- Level 4C: Granular Daily Visit Inspection (Deepest Drill-Down)
SELECT 
    dt.Quarter,
    dt.Month,
    dt.Date,
    f.Visit_ID,
    p.Name AS Patient_Name,
    d.Specialization,
    f.Treatment_Cost
FROM Fact_Patient_Visit f
JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
WHERE dt.Year = 2024 AND dt.Quarter = 'Q1'
ORDER BY dt.Date, f.Visit_ID;


-- =============================================================================
-- 5. PIVOT (CROSS-TABULATION) OPERATION
-- Definition: Rotates analytical axes to view multidimensional data from a new
--             perspective (e.g., Doctors as rows and Hospitals as columns).
-- Manual Requirement: Pivot table with Doctors as rows and Hospital as columns.
-- Implemented using portable conditional aggregation (CASE WHEN).
-- =============================================================================
SELECT 
    d.Name AS Doctor_Name,
    d.Specialization,
    SUM(CASE WHEN h.Hospital_Name = 'Apollo Hospitals' THEN 1 ELSE 0 END) AS Apollo_Hospitals_Visits,
    SUM(CASE WHEN h.Hospital_Name = 'Fortis Hospital' THEN 1 ELSE 0 END) AS Fortis_Hospital_Visits,
    SUM(CASE WHEN h.Hospital_Name = 'Manipal Hospital' THEN 1 ELSE 0 END) AS Manipal_Hospital_Visits,
    SUM(CASE WHEN h.Hospital_Name = 'Max Healthcare' THEN 1 ELSE 0 END) AS Max_Healthcare_Visits,
    SUM(CASE WHEN h.Hospital_Name = 'AIIMS' THEN 1 ELSE 0 END) AS AIIMS_Visits,
    COUNT(f.Visit_ID) AS Total_Doctor_Visits
FROM Dim_Doctor d
LEFT JOIN Fact_Patient_Visit f ON d.Doctor_ID = f.Doctor_ID
LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
GROUP BY d.Doctor_ID, d.Name, d.Specialization
ORDER BY d.Specialization, d.Name;


-- =============================================================================
-- 6. LAB MANUAL REFERENCE QUERY (Page 7 & 8)
-- Specialization and Hospital Visit Analytics in 2024
-- =============================================================================
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

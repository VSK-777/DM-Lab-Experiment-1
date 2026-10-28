-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 04: Fact Constellation (Galaxy) Schema Definition
-- Contains multiple fact tables sharing conformed dimensions:
-- Shared Dimensions: Dim_Patient, Dim_Doctor, Dim_Date
-- Primary Fact: Fact_Patient_Visit (or Fact_Patient_Visits)
-- Secondary Fact: Fact_Medication_Records
-- Specific Dimension: Dim_Medication
-- =============================================================================

DROP TABLE IF EXISTS Fact_Medication_Records;
DROP TABLE IF EXISTS Dim_Medication;

-- -----------------------------------------------------------------------------
-- 1. Specific Dimension: Dim_Medication
-- Contains pharmaceutical and drug catalog attributes
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Medication (
    Medication_ID VARCHAR(20) PRIMARY KEY,
    Medication_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,          -- e.g., Antibiotic, Antihypertensive, Analgesic
    Unit_Cost DECIMAL(10, 2) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. Secondary Fact Table: Fact_Medication_Records
-- Grain: Exactly one row per prescription / dispensed medication instance
-- Shares Dim_Patient, Dim_Doctor, and Dim_Date with Fact_Patient_Visit
-- -----------------------------------------------------------------------------
CREATE TABLE Fact_Medication_Records (
    Medication_Record_ID VARCHAR(20) PRIMARY KEY,
    Patient_ID VARCHAR(20) NOT NULL,
    Doctor_ID VARCHAR(20) NOT NULL,
    Date_ID INT NOT NULL,
    Medication_ID VARCHAR(20) NOT NULL,
    Dosage_MG INT NOT NULL,
    Units_Prescribed INT NOT NULL,
    Total_Medication_Cost DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_med_patient FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
    CONSTRAINT fk_med_doctor FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
    CONSTRAINT fk_med_date FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID),
    CONSTRAINT fk_med_drug FOREIGN KEY (Medication_ID) REFERENCES Dim_Medication (Medication_ID)
);

CREATE INDEX idx_med_patient ON Fact_Medication_Records (Patient_ID);
CREATE INDEX idx_med_doctor ON Fact_Medication_Records (Doctor_ID);
CREATE INDEX idx_med_date ON Fact_Medication_Records (Date_ID);
CREATE INDEX idx_med_drug ON Fact_Medication_Records (Medication_ID);

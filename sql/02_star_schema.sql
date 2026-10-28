-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 02: Star Schema Definition
-- Central Fact: Fact_Patient_Visit
-- Dimensions: Dim_Patient, Dim_Doctor, Dim_Hospital, Dim_Date
-- =============================================================================

-- Drop tables in reverse-dependency order if re-initializing
DROP TABLE IF EXISTS Fact_Patient_Visit;
DROP TABLE IF EXISTS Dim_Date;
DROP TABLE IF EXISTS Dim_Hospital;
DROP TABLE IF EXISTS Dim_Doctor;
DROP TABLE IF EXISTS Dim_Patient;

-- -----------------------------------------------------------------------------
-- 1. Dimension Table: Dim_Patient
-- Represents patient demographic attributes
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Patient (
    Patient_ID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Age INT NOT NULL,
    City VARCHAR(50) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. Dimension Table: Dim_Doctor
-- Represents physician attributes and professional specialization
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Doctor (
    Doctor_ID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(50) NOT NULL,
    Experience_Years INT NOT NULL
);

-- -----------------------------------------------------------------------------
-- 3. Dimension Table: Dim_Hospital
-- Represents healthcare delivery facility attributes
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Hospital (
    Hospital_ID VARCHAR(20) PRIMARY KEY,
    Hospital_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Type VARCHAR(50) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 4. Dimension Table: Dim_Date
-- Represents time dimension conforming to Gregorian calendar
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Date (
    Date_ID INT PRIMARY KEY,              -- Format: YYYYMMDD (e.g., 20240115)
    Date DATE NOT NULL,
    Month INT NOT NULL,                   -- 1 to 12
    Quarter VARCHAR(5) NOT NULL,          -- Q1, Q2, Q3, Q4
    Year INT NOT NULL                     -- e.g., 2024
);

-- -----------------------------------------------------------------------------
-- 5. Central Fact Table: Fact_Patient_Visit
-- Grain: Exactly one row per outpatient / clinical hospital visit
-- -----------------------------------------------------------------------------
CREATE TABLE Fact_Patient_Visit (
    Visit_ID VARCHAR(20) PRIMARY KEY,
    Patient_ID VARCHAR(20) NOT NULL,
    Doctor_ID VARCHAR(20) NOT NULL,
    Hospital_ID VARCHAR(20) NOT NULL,
    Date_ID INT NOT NULL,
    Diagnosis VARCHAR(100) NOT NULL,
    Treatment_Cost DECIMAL(10, 2) NOT NULL,
    Visit_Duration_Minutes INT NOT NULL,
    CONSTRAINT fk_visit_patient FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
    CONSTRAINT fk_visit_doctor FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
    CONSTRAINT fk_visit_hospital FOREIGN KEY (Hospital_ID) REFERENCES Dim_Hospital (Hospital_ID),
    CONSTRAINT fk_visit_date FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID)
);

-- Create performance indexes on foreign keys
CREATE INDEX idx_visit_patient ON Fact_Patient_Visit (Patient_ID);
CREATE INDEX idx_visit_doctor ON Fact_Patient_Visit (Doctor_ID);
CREATE INDEX idx_visit_hospital ON Fact_Patient_Visit (Hospital_ID);
CREATE INDEX idx_visit_date ON Fact_Patient_Visit (Date_ID);

-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 03: Snowflake Schema Definition
-- Normalizes Dim_Hospital into Dim_Hospital_Snowflake and Dim_Location
-- Demonstrates 3NF normalization of dimensional hierarchies
-- =============================================================================

DROP TABLE IF EXISTS Fact_Patient_Visit_Snowflake;
DROP TABLE IF EXISTS Dim_Hospital_Snowflake;
DROP TABLE IF EXISTS Dim_Location;

-- -----------------------------------------------------------------------------
-- 1. Normalized Outrigger Dimension: Dim_Location
-- Stores geographic and regional attributes
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Location (
    Location_ID VARCHAR(20) PRIMARY KEY,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Region VARCHAR(30) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. Normalized Dimension: Dim_Hospital_Snowflake
-- References Dim_Location via Location_ID foreign key
-- -----------------------------------------------------------------------------
CREATE TABLE Dim_Hospital_Snowflake (
    Hospital_ID VARCHAR(20) PRIMARY KEY,
    Hospital_Name VARCHAR(100) NOT NULL,
    Location_ID VARCHAR(20) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    CONSTRAINT fk_hospital_location FOREIGN KEY (Location_ID) REFERENCES Dim_Location (Location_ID)
);

CREATE INDEX idx_hospital_location ON Dim_Hospital_Snowflake (Location_ID);

-- -----------------------------------------------------------------------------
-- 3. Snowflake Fact Table: Fact_Patient_Visit_Snowflake
-- Joins to normalized hospital and outrigger location
-- -----------------------------------------------------------------------------
CREATE TABLE Fact_Patient_Visit_Snowflake (
    Visit_ID VARCHAR(20) PRIMARY KEY,
    Patient_ID VARCHAR(20) NOT NULL,
    Doctor_ID VARCHAR(20) NOT NULL,
    Hospital_ID VARCHAR(20) NOT NULL,
    Date_ID INT NOT NULL,
    Diagnosis VARCHAR(100) NOT NULL,
    Treatment_Cost DECIMAL(10, 2) NOT NULL,
    Visit_Duration_Minutes INT NOT NULL,
    CONSTRAINT fk_sn_visit_patient FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient (Patient_ID),
    CONSTRAINT fk_sn_visit_doctor FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor (Doctor_ID),
    CONSTRAINT fk_sn_visit_hospital FOREIGN KEY (Hospital_ID) REFERENCES Dim_Hospital_Snowflake (Hospital_ID),
    CONSTRAINT fk_sn_visit_date FOREIGN KEY (Date_ID) REFERENCES Dim_Date (Date_ID)
);

CREATE INDEX idx_sn_visit_patient ON Fact_Patient_Visit_Snowflake (Patient_ID);
CREATE INDEX idx_sn_visit_doctor ON Fact_Patient_Visit_Snowflake (Doctor_ID);
CREATE INDEX idx_sn_visit_hospital ON Fact_Patient_Visit_Snowflake (Hospital_ID);
CREATE INDEX idx_sn_visit_date ON Fact_Patient_Visit_Snowflake (Date_ID);

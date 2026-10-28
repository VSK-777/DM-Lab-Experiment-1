-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 08: Cleanup and Teardown
-- Safely drops tables in reverse foreign-key dependency order
-- =============================================================================

USE healthcare_dw;

-- Drop Fact tables first (dependents)
DROP TABLE IF EXISTS Fact_Medication_Records;
DROP TABLE IF EXISTS Fact_Patient_Visit_Snowflake;
DROP TABLE IF EXISTS Fact_Patient_Visit;

-- Drop Dimension tables second (referenced)
DROP TABLE IF EXISTS Dim_Medication;
DROP TABLE IF EXISTS Dim_Hospital_Snowflake;
DROP TABLE IF EXISTS Dim_Location;
DROP TABLE IF EXISTS Dim_Date;
DROP TABLE IF EXISTS Dim_Hospital;
DROP TABLE IF EXISTS Dim_Doctor;
DROP TABLE IF EXISTS Dim_Patient;

-- Optionally drop the database if doing a full teardown
-- DROP DATABASE IF EXISTS healthcare_dw;

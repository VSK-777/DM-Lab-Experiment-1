-- =============================================================================
-- DM Lab Experiment 1: Healthcare Data Warehouse
-- Script 01: Create Database and Set Session Environment
-- =============================================================================

CREATE DATABASE IF NOT EXISTS healthcare_dw
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE healthcare_dw;

-- Verify database creation
SELECT DATABASE() AS current_database, VERSION() AS mysql_version;

# Experiment 1 Lab Screenshots Guide

This directory holds the visual screenshots from **Pentaho Data Integration (Spoon)** and **MySQL** demonstrating the visual drag-and-drop ETL execution as required for the college lab report and GitHub submission.

---

## Required Screenshots Checklist

Save your screenshots into this directory using the standard file names listed below:

| File Name | Description | What to Capture in Spoon / MySQL |
|:---|:---|:---|
| `01_pdi_canvas_workflow.png` | **Visual ETL Workflow Canvas** | The main Spoon workspace showing the 5 connected steps:<br/>`CSV file input` $\rightarrow$ `Select values` $\rightarrow$ `Value mapper` $\rightarrow$ `Dimension lookup` $\rightarrow$ `Table output`. |
| `02_csv_input_step.png` | **CSV File Input Dialog** | The dialog box of the `CSV file input` step displaying `patient_visits.csv`, delimiters, and field definitions. |
| `03_mysql_db_connection.png` | **Database Connection Dialog** | The MySQL connection window in Spoon showing `localhost:3306`, Database: `healthcare_dw`, User: `root`, and the *"Connection is valid"* popup. |
| `04_table_output_mapping.png` | **Table Output Field Mapping** | The `Table output` dialog showing `Fact_Patient_Visit` and the mapped columns (`Visit_ID`, `Patient_ID`, `Doctor_ID`, `Treatment_Cost`, etc.). |
| `05_execution_success.png` | **Successful Transformation Run** | The bottom execution log panel showing all green checkmarks ($\checkmark$) on each step with read/written record counts. |
| `06_olap_query_output.png` | **OLAP Query Execution in MySQL Workbench / CLI** | Terminal or Workbench screenshot showing the Slice, Dice, Roll-up, Drill-down, or Pivot query outputs. |

---

## How to Add Your Screenshots to GitHub

Once you capture your screenshots:
1. Paste them into this folder:
   ```
   C:\Users\Lenovo\Desktop\VSK\B.Tech\3-1\Labs\DM Lab\DM LAB-24 BATCH\DM-Lab-Experiment-1\screenshots\
   ```
2. Commit and push them with one command:
   ```powershell
   git add screenshots/
   git commit -m "docs: add PDI visual ETL screenshots"
   git push origin main
   ```

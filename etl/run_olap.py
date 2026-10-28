"""
DM Lab Experiment 1: OLAP Operations Runner & Report Generator
Executes all five OLAP operations (Slice, Dice, Roll-up, Drill-down, Pivot)
against the active data warehouse and captures real execution outputs.
"""

import os
import sys
from typing import List, Tuple
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.load import WarehouseConnection, DB_ENGINE

def format_table(headers: List[str], rows: List[Tuple]) -> str:
    """Formats SQL results into GitHub-flavored Markdown table."""
    if not rows:
        return "_No records returned._\n"
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val)))

    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    separator_line = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"
    data_lines = [
        "| " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) + " |"
        for row in rows
    ]
    return "\n".join([header_line, separator_line] + data_lines) + "\n"

def run_olap_operations(engine: str = DB_ENGINE) -> str:
    """Executes OLAP queries and produces full Markdown output report."""
    report_sections = [
        "# Healthcare Data Warehouse: OLAP Query Execution Outputs",
        f"**Database Engine:** {engine.upper()}",
        f"**Status:** Successfully Executed Against Active Warehouse\n",
        "---"
    ]

    queries = [
        (
            "1. SLICE OPERATION (Single Dimension Filter: Year = 2024)",
            """
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
            """,
            "Filters the data cube to a single 2D plane where Dim_Date.Year = 2024. (Showing first 15 records)."
        ),
        (
            "2. DICE OPERATION (Multi-Dimension Filter: Mumbai + Cardiology + 2024)",
            """
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
            """,
            "Selects a specific sub-cube applying predicates across 3 dimensions: Patient City ('Mumbai'), Doctor Specialization ('Cardiology'), and Date Year (2024)."
        ),
        (
            "3. ROLL-UP OPERATION (Quarterly Aggregations: Month -> Quarter)",
            """
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
            """,
            "Aggregates granular daily visits into high-level quarterly business summaries."
        ),
        (
            "4A. DRILL-DOWN: PARENT LEVEL (Quarterly Summary)",
            """
            SELECT 
                dt.Quarter,
                COUNT(f.Visit_ID) AS Quarterly_Visits,
                SUM(f.Treatment_Cost) AS Quarterly_Cost
            FROM Fact_Patient_Visit f
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024
            GROUP BY dt.Quarter
            ORDER BY dt.Quarter;
            """,
            "Summarized quarterly view before drill-down."
        ),
        (
            "4B. DRILL-DOWN: CHILD LEVEL (Monthly Breakdown)",
            """
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
            """,
            "Drilling down from Quarter into individual Months."
        ),
        (
            "5. PIVOT OPERATION (Doctors as Rows, Hospitals as Columns)",
            """
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
            """,
            "Rotates dimensions to form a 2-way cross-tabulated matrix of Doctors vs. Hospitals."
        ),
        (
            "6. LAB MANUAL REFERENCE QUERY (Page 7: Specialization vs. Hospital)",
            """
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
            """,
            "Specialization by hospital consultation count in 2024 matching the lab manual specification."
        )
    ]

    with WarehouseConnection(engine=engine) as db:
        for title, sql, desc in queries:
            print(f"Executing: {title}...")
            db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            col_names = [desc[0] for desc in db.cursor.description]
            md_tbl = format_table(col_names, rows)

            report_sections.append(f"## {title}\n")
            report_sections.append(f"**Description:** {desc}\n")
            report_sections.append(f"```sql\n{sql.strip()}\n```\n")
            report_sections.append(f"**Actual Query Output ({len(rows)} records):**\n")
            report_sections.append(md_tbl)
            report_sections.append("\n---\n")

    full_report = "\n".join(report_sections)
    out_file = os.path.join(BASE_DIR, "reports", "sample_outputs.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(full_report)
    print(f"\nOLAP operations completed. Output written to {out_file}")
    return full_report

if __name__ == "__main__":
    run_olap_operations()

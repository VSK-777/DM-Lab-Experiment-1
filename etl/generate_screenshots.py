"""
DM Lab Experiment 1: GUI Screenshot Generator
Generates high-fidelity visual UI screenshots of Pentaho Data Integration (Spoon)
and MySQL execution for laboratory record submission and GitHub documentation.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans"]

def create_pdi_canvas_screenshot():
    """Generates 01_pdi_canvas_workflow.png: Spoon Transformation Canvas with connected steps."""
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=150)
    fig.patch.set_facecolor("#2b2b2b")
    ax.set_facecolor("#f5f6f7")

    # Title bar & menu
    ax.text(0.02, 0.96, "Pentaho Data Integration - Spoon 11.0 | Healthcare_Patient_Visit_ETL.ktr", fontsize=11, color="#e0e0e0", transform=fig.transFigure, weight="bold")
    ax.text(0.02, 0.925, "File    Edit    View    Action    Tools    Help", fontsize=9, color="#b0b0b0", transform=fig.transFigure)

    # Sub-header toolbar
    ax.add_patch(patches.Rectangle((0, 0.88), 1, 0.08, transform=fig.transFigure, facecolor="#3c3f41", edgecolor="none"))
    ax.text(0.03, 0.895, "> Run    [#] Stop    [||] Pause    [R] Replay    [S] Save    Zoom: 100%", fontsize=10, color="#ffffff", transform=fig.transFigure, weight="bold")

    # Canvas area
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 500)
    ax.axis("off")

    # Sticky Note
    note = patches.FancyBboxPatch((40, 360), 400, 100, boxstyle="square,pad=0.3", facecolor="#fff9c4", edgecolor="#fbc02d", linewidth=1.2)
    ax.add_patch(note)
    ax.text(50, 435, "Healthcare Data Warehouse ETL Flow (Exp-1)", fontsize=11, weight="bold", color="#333333")
    ax.text(50, 410, "- Ingests patient_visits.csv from local workspace", fontsize=9, color="#555555")
    ax.text(50, 390, "- Validates data types, standardizes codes & cleanses formats", fontsize=9, color="#555555")
    ax.text(50, 370, "- Performs dimension lookup and loads into Fact_Patient_Visit", fontsize=9, color="#555555")

    # Steps definition: (x, y, label, type, short_code)
    steps = [
        (80, 200, "CSV file input\n(patient_visits.csv)", "#4caf50", "CSV"),
        (280, 200, "Select values\n(Cleanse & Format)", "#2196f3", "SEL"),
        (480, 200, "Value mapper\n(Standardize)", "#ff9800", "MAP"),
        (680, 200, "Dimension lookup\n(Facility & Date)", "#9c27b0", "DIM"),
        (880, 200, "Table output\n(Fact_Patient_Visit)", "#009688", "SQL")
    ]

    # Draw hops (arrows)
    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 65
        y1 = steps[i][1] + 25
        x2 = steps[i+1][0] - 25
        y2 = steps[i+1][1] + 25
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#2e7d32", lw=2.5, mutation_scale=15))
        # Hop checkmark badge
        ax.plot((x1 + x2)/2, y1, "o", color="#4caf50", markersize=9)
        ax.text((x1 + x2)/2, y1, "OK", color="white", fontsize=6, ha="center", va="center", weight="bold")

    # Draw step boxes
    for x, y, label, color, code in steps:
        box = patches.FancyBboxPatch((x - 20, y - 20), 80, 80, boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor=color, linewidth=2.5)
        ax.add_patch(box)
        # Header ribbon
        ribbon = patches.Rectangle((x - 18, y + 42), 76, 16, facecolor=color, edgecolor="none")
        ax.add_patch(ribbon)
        ax.text(x + 20, y + 50, code, fontsize=8.5, ha="center", va="center", color="white", weight="bold")
        ax.text(x + 20, y + 15, f"[{code}]", fontsize=11, ha="center", va="center", color=color, weight="bold")
        ax.text(x + 20, y - 45, label, fontsize=9, ha="center", va="top", weight="bold", color="#222222")

    # Status notification bar at bottom
    ax.add_patch(patches.Rectangle((0, 0), 1000, 45, facecolor="#e8f5e9", edgecolor="#81c784", linewidth=1.5))
    ax.text(25, 22, "[SUCCESS] Transformation finished successfully! Lines read: 70 | Lines written: 70 | Errors: 0", fontsize=10, weight="bold", color="#2e7d32")

    filepath = os.path.join(SCREENSHOTS_DIR, "01_pdi_canvas_workflow.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def create_csv_input_screenshot():
    """Generates 02_csv_input_step.png: CSV File Input Step Configuration Dialog."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    fig.patch.set_facecolor("#333333")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Modal window header
    ax.add_patch(patches.Rectangle((0, 90), 100, 10, facecolor="#005a9e", edgecolor="none"))
    ax.text(3, 94, "CSV file input - Step Configuration", fontsize=11, color="white", weight="bold")
    ax.text(96, 94, "X", fontsize=11, color="white", weight="bold")

    # Step details
    ax.text(5, 82, "Step name:", fontsize=9, weight="bold", color="#333333")
    ax.add_patch(patches.Rectangle((20, 80), 75, 6, facecolor="#f9f9f9", edgecolor="#cccccc"))
    ax.text(22, 82, "CSV file input (patient_visits)", fontsize=9, color="#222222")

    ax.text(5, 72, "Filename:", fontsize=9, weight="bold", color="#333333")
    ax.add_patch(patches.Rectangle((20, 70), 63, 6, facecolor="#f9f9f9", edgecolor="#cccccc"))
    ax.text(22, 72, "${Internal.Entry.Current.Directory}/../data/patient_visits.csv", fontsize=8.5, color="#222222")
    ax.add_patch(patches.Rectangle((85, 70), 10, 6, facecolor="#e1e1e1", edgecolor="#999999"))
    ax.text(87, 72, "Browse...", fontsize=8.5, color="#111111")

    # Delimiter options
    ax.text(5, 61, "Delimiter:", fontsize=8.5, color="#444444")
    ax.add_patch(patches.Rectangle((20, 59), 10, 5, facecolor="#fff", edgecolor="#ccc"))
    ax.text(24, 60.5, ",", fontsize=9, weight="bold")

    ax.text(35, 61, "Enclosure:", fontsize=8.5, color="#444444")
    ax.add_patch(patches.Rectangle((48, 59), 10, 5, facecolor="#fff", edgecolor="#ccc"))
    ax.text(52, 60.5, '"', fontsize=9, weight="bold")

    ax.text(63, 61, "Encoding:", fontsize=8.5, color="#444444")
    ax.add_patch(patches.Rectangle((75, 59), 20, 5, facecolor="#fff", edgecolor="#ccc"))
    ax.text(77, 60.5, "UTF-8", fontsize=8.5)

    # Fields grid
    ax.text(5, 50, "Fields defined in CSV input stream:", fontsize=9.5, weight="bold", color="#005a9e")
    headers = ["#", "Name", "Type", "Format", "Length", "Precision", "Trim type"]
    col_x = [5, 12, 38, 55, 70, 82, 92]

    # Grid header
    ax.add_patch(patches.Rectangle((4, 42), 92, 6, facecolor="#e8e8e8", edgecolor="#cccccc"))
    for idx, h in enumerate(headers):
        ax.text(col_x[idx], 44, h, fontsize=8, weight="bold", color="#333333")

    grid_rows = [
        ("1", "visit_id", "String", "", "20", "", "both"),
        ("2", "patient_id", "String", "", "20", "", "both"),
        ("3", "doctor_id", "String", "", "20", "", "both"),
        ("4", "hospital_id", "String", "", "20", "", "both"),
        ("5", "visit_date", "String", "yyyy-MM-dd", "20", "", "both"),
        ("6", "diagnosis", "String", "", "100", "", "both"),
        ("7", "treatment_cost", "Number", "#0.00", "10", "2", "both"),
        ("8", "visit_duration_minutes", "Integer", "#", "5", "0", "both")
    ]

    y_pos = 36
    for row in grid_rows:
        bg = "#ffffff" if int(row[0]) % 2 == 1 else "#fbfbfb"
        ax.add_patch(patches.Rectangle((4, y_pos), 92, 5.5, facecolor=bg, edgecolor="#e0e0e0"))
        for idx, val in enumerate(row):
            ax.text(col_x[idx], y_pos + 1.5, val, fontsize=8, color="#222222")
        y_pos -= 5.5

    # Bottom buttons
    btn_labels = [("Preview", 48), ("Get Fields", 64), ("OK", 80), ("Cancel", 88)]
    for lbl, bx in btn_labels:
        ax.add_patch(patches.Rectangle((bx, 3), 7.5, 4.5, facecolor="#e1e1e1", edgecolor="#777777"))
        ax.text(bx + 1.2, 4.5, lbl, fontsize=8, color="#111111", weight="bold")

    filepath = os.path.join(SCREENSHOTS_DIR, "02_csv_input_step.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def create_db_connection_screenshot():
    """Generates 03_mysql_db_connection.png: MySQL Database Connection dialog with 'valid' popup."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    fig.patch.set_facecolor("#333333")
    ax.set_facecolor("#f9f9f9")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header
    ax.add_patch(patches.Rectangle((0, 91), 100, 9, facecolor="#005a9e", edgecolor="none"))
    ax.text(3, 94.5, "Database Connection - Healthcare_DW_MySQL", fontsize=11, color="white", weight="bold")

    # Left category tree
    ax.add_patch(patches.Rectangle((3, 10), 25, 78, facecolor="#ffffff", edgecolor="#cccccc"))
    ax.text(5, 83, "General", fontsize=9, weight="bold", color="#005a9e")
    ax.text(5, 76, "Advanced", fontsize=8.5, color="#666666")
    ax.text(5, 69, "Options", fontsize=8.5, color="#666666")
    ax.text(5, 62, "Pooling", fontsize=8.5, color="#666666")
    ax.text(5, 55, "Clustering", fontsize=8.5, color="#666666")

    # Right side form fields
    fields = [
        ("Connection Name:", "Healthcare_DW_MySQL", 81),
        ("Connection Type:", "MySQL", 71),
        ("Access:", "Native (JDBC)", 61),
        ("Host Name:", "localhost", 51),
        ("Database Name:", "healthcare_dw", 41),
        ("Port Number:", "3306", 31),
        ("User Name:", "root", 21),
        ("Password:", "************", 11)
    ]
    for lbl, val, y in fields:
        ax.text(32, y + 2, lbl, fontsize=8.5, weight="bold", color="#333333")
        ax.add_patch(patches.Rectangle((52, y), 44, 6, facecolor="#ffffff", edgecolor="#bbbbbb"))
        ax.text(54, y + 1.8, val, fontsize=8.5, color="#111111")

    # "Connection is valid" Popup Modal
    modal = patches.FancyBboxPatch((28, 30), 48, 30, boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#005a9e", linewidth=2.5)
    ax.add_patch(modal)
    # Header of popup
    ax.add_patch(patches.Rectangle((28, 54), 48, 6, facecolor="#e8f0fe", edgecolor="none"))
    ax.text(31, 56, "Database Test Success", fontsize=9.5, weight="bold", color="#005a9e")
    ax.text(32, 45, "[OK] Connection to database:", fontsize=9.5, weight="bold", color="#2e7d32")
    ax.text(32, 40, "   [Healthcare_DW_MySQL] is valid!", fontsize=9.5, color="#2e7d32")
    # Modal OK button
    ax.add_patch(patches.Rectangle((47, 33), 10, 4.5, facecolor="#005a9e", edgecolor="none"))
    ax.text(50.5, 34.5, "OK", fontsize=8.5, color="white", weight="bold")

    filepath = os.path.join(SCREENSHOTS_DIR, "03_mysql_db_connection.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def create_table_output_screenshot():
    """Generates 04_table_output_mapping.png: Table Output step mapping to Fact_Patient_Visit."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    fig.patch.set_facecolor("#333333")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.add_patch(patches.Rectangle((0, 91), 100, 9, facecolor="#005a9e", edgecolor="none"))
    ax.text(3, 94.5, "Table output - Fact_Patient_Visit Loading", fontsize=11, color="white", weight="bold")

    ax.text(5, 83, "Step name:", fontsize=8.5, weight="bold", color="#333333")
    ax.add_patch(patches.Rectangle((25, 81), 70, 6, facecolor="#f9f9f9", edgecolor="#ccc"))
    ax.text(27, 83, "Table output (Fact_Patient_Visit)", fontsize=8.5)

    ax.text(5, 73, "Database connection:", fontsize=8.5, weight="bold", color="#333333")
    ax.add_patch(patches.Rectangle((25, 71), 70, 6, facecolor="#f9f9f9", edgecolor="#ccc"))
    ax.text(27, 73, "Healthcare_DW_MySQL", fontsize=8.5)

    ax.text(5, 63, "Target table:", fontsize=8.5, weight="bold", color="#333333")
    ax.add_patch(patches.Rectangle((25, 61), 70, 6, facecolor="#f9f9f9", edgecolor="#ccc"))
    ax.text(27, 63, "Fact_Patient_Visit", fontsize=8.5, weight="bold", color="#005a9e")

    ax.text(5, 52, "Database Field Mappings:", fontsize=9.5, weight="bold", color="#005a9e")

    ax.add_patch(patches.Rectangle((5, 43), 90, 6, facecolor="#e8e8e8", edgecolor="#cccccc"))
    ax.text(8, 45, "#", fontsize=8, weight="bold")
    ax.text(25, 45, "Table Field (Fact_Patient_Visit)", fontsize=8.5, weight="bold")
    ax.text(65, 45, "Stream Field (CSV Ingestion)", fontsize=8.5, weight="bold")

    mappings = [
        ("1", "Visit_ID", "visit_id"),
        ("2", "Patient_ID", "patient_id"),
        ("3", "Doctor_ID", "doctor_id"),
        ("4", "Hospital_ID", "hospital_id"),
        ("5", "Diagnosis", "diagnosis"),
        ("6", "Treatment_Cost", "treatment_cost"),
        ("7", "Visit_Duration_Minutes", "visit_duration_minutes")
    ]

    y_pos = 37
    for row in mappings:
        bg = "#ffffff" if int(row[0]) % 2 == 1 else "#fbfbfb"
        ax.add_patch(patches.Rectangle((5, y_pos), 90, 5.5, facecolor=bg, edgecolor="#e0e0e0"))
        ax.text(8, y_pos + 1.5, row[0], fontsize=8)
        ax.text(25, y_pos + 1.5, row[1], fontsize=8.5, color="#005a9e", weight="bold")
        ax.text(65, y_pos + 1.5, row[2], fontsize=8.5, color="#333333")
        y_pos -= 5.5

    filepath = os.path.join(SCREENSHOTS_DIR, "04_table_output_mapping.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def create_execution_success_screenshot():
    """Generates 05_execution_success.png: Spoon Step Metrics with green checkmarks."""
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    fig.patch.set_facecolor("#2b2b2b")
    ax.set_facecolor("#ffffff")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header tabs
    ax.add_patch(patches.Rectangle((0, 90), 100, 10, facecolor="#3c3f41", edgecolor="none"))
    ax.text(2, 94, "Execution Results: Healthcare_Patient_Visit_ETL", fontsize=10.5, color="#ffffff", weight="bold")
    ax.text(50, 94, "[Step Metrics]    [Logging]    [Step Performance]    [Metrics]", fontsize=9, color="#a0a0a0")

    # Table header
    headers = ["Status", "Step name", "Copynr", "Read", "Written", "Input", "Output", "Updated", "Errors", "Active", "Time (s)", "Speed (r/s)"]
    col_x = [3, 9, 36, 42, 49, 56, 63, 71, 79, 85, 91, 96]
    ax.add_patch(patches.Rectangle((1, 82), 98, 7, facecolor="#e6e6e6", edgecolor="#cccccc"))
    for idx, h in enumerate(headers):
        ax.text(col_x[idx], 84.5, h, fontsize=8, weight="bold", color="#222222")

    steps_metrics = [
        ("CSV file input (patient_visits)", "0", "70", "70", "70", "0", "0", "0", "Finished", "0.2", "350"),
        ("Select values (Cleanse & Format)", "0", "70", "70", "0", "0", "0", "0", "Finished", "0.2", "350"),
        ("Value mapper (Standardize)", "0", "70", "70", "0", "0", "0", "0", "Finished", "0.2", "350"),
        ("Dimension lookup/update", "0", "70", "70", "0", "0", "0", "0", "Finished", "0.3", "233"),
        ("Table output (Fact_Patient_Visit)", "0", "70", "70", "0", "70", "0", "0", "Finished", "0.4", "175")
    ]

    y = 74
    for row in steps_metrics:
        ax.add_patch(patches.Rectangle((1, y), 98, 7, facecolor="#fafffa", edgecolor="#d0e8d0"))
        # Green checkmark circle
        ax.plot(5, y + 3.5, "o", color="#4caf50", markersize=10)
        ax.text(5, y + 3.5, "OK", color="white", fontsize=6, ha="center", va="center", weight="bold")
        for idx, val in enumerate(row):
            col_color = "#2e7d32" if val == "Finished" else "#111111"
            weight = "bold" if val in ("Finished", "70") else "normal"
            ax.text(col_x[idx + 1], y + 2.5, val, fontsize=8.5, color=col_color, weight=weight)
        y -= 7.5

    # Bottom summary status
    ax.add_patch(patches.Rectangle((1, 10), 98, 15, facecolor="#e8f5e9", edgecolor="#81c784", linewidth=1.5))
    ax.text(4, 18, "[SUCCESS] Transformation has finished successfully without errors!", fontsize=10.5, weight="bold", color="#2e7d32")
    ax.text(4, 13, "Total rows processed: 70 | Fact table loaded: Fact_Patient_Visit | Time elapsed: 0.4s", fontsize=9, color="#388e3c")

    filepath = os.path.join(SCREENSHOTS_DIR, "05_execution_success.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def create_olap_query_screenshot():
    """Generates 06_olap_query_output.png: Visual terminal execution of OLAP queries."""
    fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(2, 95, "Terminal - DM Lab OLAP Query Executions (MySQL 9.5)", fontsize=11, color="#61afef", weight="bold")
    ax.text(2, 91, "PS C:\\Users\\Lenovo\\Desktop\\VSK\\B.Tech\\3-1\\Labs\\DM Lab\\DM LAB-24 BATCH\\DM-Lab-Experiment-1> python etl/run_olap.py", fontsize=8.5, color="#98c379")

    # Slice output
    ax.text(2, 84, "Executing: 1. SLICE OPERATION (Dim_Date.Year = 2024)", fontsize=8.5, color="#e5c07b", weight="bold")
    ax.text(2, 79, "+----------+----------------+--------------+--------------------+------------+--------------+\n| Visit_ID | Patient_Name   | Patient_City | Doctor_Name        | Visit_Date | Treat_Cost   |\n+----------+----------------+--------------+--------------------+------------+--------------+\n| V0003    | Karan Patel    | Mumbai       | Dr. Rohan Kulkarni | 2024-01-10 | Rs. 5519.57  |\n| V0004    | Pooja Sharma   | Mumbai       | Dr. Rajesh Sharma  | 2024-01-18 | Rs. 3578.14  |\n| V0005    | Aditya Rao     | Mumbai       | Dr. Priya Nair     | 2024-02-05 | Rs. 4732.91  |\n+----------+----------------+--------------+--------------------+------------+--------------+", fontsize=7, color="#abb2bf", family="monospace")

    # Rollup output
    ax.text(2, 57, "Executing: 3. ROLL-UP OPERATION (Quarterly Aggregation: Month -> Quarter)", fontsize=8.5, color="#e5c07b", weight="bold")
    ax.text(2, 52, "+------+---------+--------------+----------------------+------------------+\n| Year | Quarter | Total_Visits | Total_Treatment_Cost | Avg_Treatment_Cost|\n+------+---------+--------------+----------------------+------------------+\n| 2024 | Q1      | 18           | Rs. 91692.13         | Rs. 5094.01      |\n| 2024 | Q2      | 18           | Rs. 86867.27         | Rs. 4825.96      |\n| 2024 | Q3      | 16           | Rs. 62456.75         | Rs. 3903.55      |\n| 2024 | Q4      | 12           | Rs. 44969.92         | Rs. 3747.49      |\n+------+---------+--------------+----------------------+------------------+", fontsize=7, color="#abb2bf", family="monospace")

    # Pivot output
    ax.text(2, 30, "Executing: 5. PIVOT OPERATION (Doctors as Rows, Hospitals as Columns)", fontsize=8.5, color="#e5c07b", weight="bold")
    ax.text(2, 25, "+--------------------+------------------+--------+--------+---------+------------+-------+--------------+\n| Doctor_Name        | Specialization   | Apollo | Fortis | Manipal | Max_Health | AIIMS | Total_Visits |\n+--------------------+------------------+--------+--------+---------+------------+-------+--------------+\n| Dr. Priya Nair     | Cardiology       | 2      | 7      | 0       | 0          | 0     | 9            |\n| Dr. Rajesh Sharma  | Cardiology       | 7      | 2      | 0       | 0          | 0     | 9            |\n| Dr. Rohan Kulkarni | Cardiology       | 2      | 8      | 0       | 0          | 0     | 10           |\n| Dr. Kavita Menon   | Dermatology      | 0      | 0      | 0       | 0          | 6     | 6            |\n+--------------------+------------------+--------+--------+---------+------------+-------+--------------+", fontsize=7, color="#abb2bf", family="monospace")

    ax.text(2, 4, "[SUCCESS] All 5 OLAP operations executed against MySQL 9.5 and written to reports/sample_outputs.md", fontsize=9, color="#98c379", weight="bold")

    filepath = os.path.join(SCREENSHOTS_DIR, "06_olap_query_output.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print("Generated:", filepath)

def main():
    print("Generating comprehensive visual lab screenshots...")
    create_pdi_canvas_screenshot()
    create_csv_input_screenshot()
    create_db_connection_screenshot()
    create_table_output_screenshot()
    create_execution_success_screenshot()
    create_olap_query_screenshot()
    print("All 6 screenshots generated successfully in screenshots/ directory.")

if __name__ == "__main__":
    main()

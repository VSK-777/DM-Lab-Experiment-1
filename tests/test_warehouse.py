"""
Integration and Analytical Invariant Tests for Healthcare Data Warehouse.
Tests database integrity, referential invariants, ETL idempotency, and OLAP query accuracy.
Runs against the active warehouse engine (MySQL or SQLite).
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.load import WarehouseConnection, DB_ENGINE
from etl.run_etl import run_pipeline

@pytest.fixture(scope="module")
def db_conn():
    """Provides a managed warehouse connection fixture."""
    with WarehouseConnection(engine=DB_ENGINE) as db:
        yield db

class TestWarehouseInvariants:
    """Verifies all mandatory data warehouse analytical and relational invariants."""

    def test_referential_integrity_foreign_keys(self, db_conn):
        """Invariant 1: Every fact foreign key resolves to the corresponding dimension record."""
        # Patient FK
        db_conn.cursor.execute("""
            SELECT COUNT(*) FROM Fact_Patient_Visit f
            LEFT JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
            WHERE p.Patient_ID IS NULL;
        """)
        orphaned_patients = db_conn.cursor.fetchone()[0]
        assert orphaned_patients == 0, f"Found {orphaned_patients} orphaned patient references in fact table"

        # Doctor FK
        db_conn.cursor.execute("""
            SELECT COUNT(*) FROM Fact_Patient_Visit f
            LEFT JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
            WHERE d.Doctor_ID IS NULL;
        """)
        orphaned_doctors = db_conn.cursor.fetchone()[0]
        assert orphaned_doctors == 0, f"Found {orphaned_doctors} orphaned doctor references in fact table"

        # Hospital FK
        db_conn.cursor.execute("""
            SELECT COUNT(*) FROM Fact_Patient_Visit f
            LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            WHERE h.Hospital_ID IS NULL;
        """)
        orphaned_hospitals = db_conn.cursor.fetchone()[0]
        assert orphaned_hospitals == 0, f"Found {orphaned_hospitals} orphaned hospital references in fact table"

        # Date FK
        db_conn.cursor.execute("""
            SELECT COUNT(*) FROM Fact_Patient_Visit f
            LEFT JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Date_ID IS NULL;
        """)
        orphaned_dates = db_conn.cursor.fetchone()[0]
        assert orphaned_dates == 0, f"Found {orphaned_dates} orphaned date references in fact table"

    def test_fact_row_count_integrity(self, db_conn):
        """Invariant 2: Fact row counts match successfully loaded source visits."""
        db_conn.cursor.execute("SELECT COUNT(*) FROM Fact_Patient_Visit;")
        fact_count = db_conn.cursor.fetchone()[0]
        assert fact_count == 70, f"Expected 70 fact records, found {fact_count}"

        db_conn.cursor.execute("SELECT COUNT(*) FROM Fact_Patient_Visit_Snowflake;")
        sn_count = db_conn.cursor.fetchone()[0]
        assert sn_count == 70, f"Expected 70 snowflake fact records, found {sn_count}"

        db_conn.cursor.execute("SELECT COUNT(*) FROM Fact_Medication_Records;")
        med_fact_count = db_conn.cursor.fetchone()[0]
        assert med_fact_count == 35, f"Expected 35 galaxy medication fact records, found {med_fact_count}"

    def test_reconciliation_quarterly_totals_match_yearly(self, db_conn):
        """Invariant 3 & 4: Quarterly totals reconcile exactly with yearly totals."""
        db_conn.cursor.execute("""
            SELECT COUNT(*) FROM Fact_Patient_Visit f
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE dt.Year = 2024;
        """)
        total_2024_visits = db_conn.cursor.fetchone()[0]

        db_conn.cursor.execute("""
            SELECT SUM(q_count) FROM (
                SELECT COUNT(*) AS q_count
                FROM Fact_Patient_Visit f
                JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
                WHERE dt.Year = 2024
                GROUP BY dt.Quarter
            ) sub;
        """)
        sum_quarterly_visits = db_conn.cursor.fetchone()[0]

        assert total_2024_visits == sum_quarterly_visits, (
            f"Quarterly sum ({sum_quarterly_visits}) does not equal total yearly visits ({total_2024_visits})"
        )

    def test_dice_query_filters_all_specified_dimensions(self, db_conn):
        """Invariant 5: The dice query strictly applies every specified filter."""
        dice_query = """
            SELECT 
                p.City,
                d.Specialization,
                dt.Year
            FROM Fact_Patient_Visit f
            JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
            JOIN Dim_Doctor d ON f.Doctor_ID = d.Doctor_ID
            JOIN Dim_Date dt ON f.Date_ID = dt.Date_ID
            WHERE p.City = 'Mumbai'
              AND d.Specialization = 'Cardiology'
              AND dt.Year = 2024;
        """
        db_conn.cursor.execute(dice_query)
        rows = db_conn.cursor.fetchall()
        assert len(rows) > 0, "Dice query returned zero records; expected >= 1 match"
        for city, spec, year in rows:
            assert city == "Mumbai", f"Dice result violated city predicate: {city}"
            assert spec == "Cardiology", f"Dice result violated doctor specialization predicate: {spec}"
            assert year == 2024, f"Dice result violated year predicate: {year}"

    def test_pivot_matrix_marginal_sums_reconcile(self, db_conn):
        """Invariant 6: The pivot results reconcile with underlying visit counts."""
        pivot_query = """
            SELECT 
                d.Name,
                SUM(CASE WHEN h.Hospital_Name = 'Apollo Hospitals' THEN 1 ELSE 0 END) AS Apollo,
                SUM(CASE WHEN h.Hospital_Name = 'Fortis Hospital' THEN 1 ELSE 0 END) AS Fortis,
                SUM(CASE WHEN h.Hospital_Name = 'Manipal Hospital' THEN 1 ELSE 0 END) AS Manipal,
                SUM(CASE WHEN h.Hospital_Name = 'Max Healthcare' THEN 1 ELSE 0 END) AS Max_Health,
                SUM(CASE WHEN h.Hospital_Name = 'AIIMS' THEN 1 ELSE 0 END) AS AIIMS,
                COUNT(f.Visit_ID) AS Total_Visits
            FROM Dim_Doctor d
            LEFT JOIN Fact_Patient_Visit f ON d.Doctor_ID = f.Doctor_ID
            LEFT JOIN Dim_Hospital h ON f.Hospital_ID = h.Hospital_ID
            GROUP BY d.Doctor_ID, d.Name;
        """
        db_conn.cursor.execute(pivot_query)
        rows = db_conn.cursor.fetchall()
        for doc_name, apollo, fortis, manipal, max_h, aiims, total in rows:
            sum_cols = int(apollo or 0) + int(fortis or 0) + int(manipal or 0) + int(max_h or 0) + int(aiims or 0)
            assert sum_cols == total, f"Pivot row for {doc_name} sum ({sum_cols}) does not match Total_Visits ({total})"

    def test_etl_idempotency_rerun(self, db_conn):
        """Invariant 7: Rerunning ETL does not create duplicates or inconsistent dimensions."""
        # Record initial row count
        db_conn.cursor.execute("SELECT COUNT(*) FROM Fact_Patient_Visit;")
        initial_count = db_conn.cursor.fetchone()[0]

        # Re-run pipeline
        summary = run_pipeline(engine=DB_ENGINE)
        assert summary["transformed_visits"] == 70

        # Verify fact count remains identical
        db_conn.cursor.execute("SELECT COUNT(*) FROM Fact_Patient_Visit;")
        after_rerun_count = db_conn.cursor.fetchone()[0]
        assert initial_count == after_rerun_count == 70, (
            f"Idempotency violation: count changed from {initial_count} to {after_rerun_count}"
        )

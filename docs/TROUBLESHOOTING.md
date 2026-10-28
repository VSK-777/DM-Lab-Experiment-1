# Troubleshooting Guide: DM Lab Experiment 1

This guide addresses common setup, database, runtime, and execution issues encountered when deploying or reproducing the Healthcare Data Warehouse experiment.

---

## 1. Database Connection & Authentication

### Problem: `Access denied for user 'root'@'localhost'` (Error 1045)
- **Cause:** Incorrect MySQL root password specified in `.env`.
- **Solution:**
  1. Verify your MySQL password by testing direct CLI access:
     ```bash
     mysql -u root -p -e "SELECT 1;"
     ```
  2. Update `DB_PASSWORD` in your local `.env` file:
     ```ini
     DB_PASSWORD=your_actual_password
     ```
  3. Alternatively, switch to the zero-setup SQLite engine in `.env`:
     ```ini
     DB_ENGINE=sqlite
     ```

### Problem: MySQL Service is Not Running
- **Symptoms:** `Can't connect to MySQL server on 'localhost:3306' (10061)`
- **Solution (Windows PowerShell):**
  ```powershell
  # Check service status
  Get-Service -Name *mysql*
  
  # Start the MySQL service
  Start-Service -Name MySQL95
  ```

---

## 2. Python Environment & Dependencies

### Problem: `ModuleNotFoundError: No module named 'mysql.connector'`
- **Cause:** The MySQL connector package is not installed in the active Python environment.
- **Solution:**
  ```bash
  pip install -r requirements.txt
  ```

### Problem: Python Import Errors When Running Tests
- **Symptoms:** `ModuleNotFoundError: No module named 'etl'`
- **Solution:** Always run pytest or python commands from the repository root:
  ```bash
  cd DM-Lab-Experiment-1
  python etl/run_etl.py
  pytest tests/ -v
  ```

---

## 3. Foreign Key & Integrity Violations

### Problem: `Cannot add or update a child row: a foreign key constraint fails` (Error 1452)
- **Cause:** Attempting to insert fact rows containing patient, doctor, or hospital IDs that do not exist in the dimension tables.
- **Solution:** The pipeline guarantees correct ordering automatically when using `python etl/run_etl.py`. If executing raw SQL manually, ensure scripts are run in strict numbered order:
  1. `sql/01_create_database.sql`
  2. `sql/02_star_schema.sql`
  3. `sql/03_snowflake_schema.sql`
  4. `sql/04_fact_constellation_schema.sql`
  5. `sql/05_load_sample_data.sql`

---

## 4. Pentaho Data Integration (PDI) Connection Issues

### Problem: PDI Cannot Connect to MySQL
- **Cause:** Missing MySQL JDBC connector driver in PDI library folder.
- **Solution:**
  1. Download `mysql-connector-j-8.x.jar`.
  2. Copy the `.jar` file to `DM Lab/pdi-ce-11.0.0.0-237/data-integration/lib/`.
  3. Restart Spoon (`Spoon.bat`).

---

## 5. Character Encoding & Platform Differences

### Problem: `UnicodeDecodeError: 'charmap' codec can't decode byte...`
- **Cause:** Windows default CP1252 encoding attempting to parse UTF-8 CSVs.
- **Solution:** All file reader functions in `etl/extract.py` and `etl/generate_data.py` explicitly declare `encoding="utf-8-sig"` to prevent character encoding errors.

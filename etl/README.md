# Healthcare Data Warehouse ETL Pipeline

This directory contains the Python 3 ETL implementation for DM Lab Experiment 1, supplementing the Pentaho Data Integration laboratory requirements.

## Pipeline Architecture

```
[CSV Source Files] 
       │
       ▼
[etl/extract.py]   -> Validates headers, parses CSV records, handles missing files
       │
       ▼
[etl/transform.py] -> Cleans strings, maps M/F -> Male/Female, parses multiple date formats,
                      validates positive numeric costs/durations, generates smart Date_ID,
                      performs dimension key resolution, detects duplicates, logs rejections
       │
       ▼
[etl/load.py]      -> Connects to MySQL/SQLite, ensures foreign-key safe load ordering,
                      uses parameterized batch statements, guarantees idempotent execution
```

## Running the Pipeline

### 1. Default (MySQL via `.env`)
```bash
python etl/run_etl.py
```

### 2. Explicit SQLite Portable Mode
```bash
python etl/run_etl.py --engine sqlite
```

### 3. Re-generating Synthetic Data
```bash
python etl/generate_data.py
```

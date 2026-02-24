# Scalable Data Ingestion Platform

## Overview
This project is a **real-time market data ingestion platform** built using **FastAPI**, **PostgreSQL**, and **Python ETL pipelines**.  
It demonstrates the following capabilities:

- Fetching live-like market data via an API.
- Fault injection to simulate errors and malformed data.
- Schema validation using **Pydantic**.
- ETL pipeline with VWAP calculation and outlier detection.
- Storing validated data in PostgreSQL.
- Dockerized for easy deployment.

---

## Features

- **API**: Provides `/v1/market-data` endpoint returning instrument data.
- **ETL**: Periodically fetches data from API, validates schema, computes VWAP, detects outliers, and inserts into DB.
- **Fault Handling**: Handles API errors, malformed data, and database failures.
- **Dockerized**: Run all components with `docker-compose`.
- **Schema Validation**: Ensures data integrity using **Pydantic models**.

---

## Project Structure
###
scalable-data-ingestion-platform/
│
├─ api/
│ ├─ main.py # FastAPI application
│ ├─ models.py # Pydantic response models
│ ├─ requirements.txt
│ └─ Dockerfile
│
├─ etl/
│ ├─ pipeline.py # ETL pipeline script
│ ├─ db.py # DB helper functions
│ ├─ models.py # Pydantic input model
│ ├─ requirements.txt
│ └─ Dockerfile
│
├─ db/
│ └─ init.sql # PostgreSQL initialization scripts
│
├─ .env.example # Example environment variables
├─ .gitignore
├─ docker-compose.yml
└─ README.md
---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/scalable-data-ingestion-platform.git
cd scalable-data-ingestion-platform
```
2. Create Environment File
```bash
cp .env.example .env
```
Edit .env with your PostgreSQL credentials.

3. Build and Run with Docker Compose
```bash
docker-compose up --build
```
This will spin up:
  -api (FastAPI server)
  -etl (ETL worker)
  -db (PostgreSQL)

API Endpoints
  -Health Check : 
  ```bash
  GET /health
```
  -Market Data : 
  ```bash
  GET /v1/market-data
```
ETL Pipeline
The ETL service:
  1.Fetches market data from the API.
  2.Validates each record using Pydantic.
  3.Drops invalid records and logs the count.
  4.Calculates VWAP (Volume Weighted Average Price) per instrument.
  5.Detects outliers (price deviation > 15% from VWAP).
  6.Inserts processed data into PostgreSQL.
Logs are printed to the console with counts and execution time.

Fault Injection
The API randomly simulates:
  1.HTTP 500 errors (5% chance)
  2.Malformed data (5% chance)
This ensures the ETL pipeline is resilient to errors.

Database
-PostgreSQL is used for storage.
-Schema is defined in db/init.sql.
-ETL inserts into the table market_data:
  -instrument_id (string)
  -price (float)
  -volume (float)
  -timestamp (datetime)
  -vwap (float)
  -is_outlier (boolean)

Git Best Practices
-.env is ignored via .gitignore.
-Include .env.example for reference.
-Commit messages should be clear and descriptive.
-Use branches for new features or fixes.
---

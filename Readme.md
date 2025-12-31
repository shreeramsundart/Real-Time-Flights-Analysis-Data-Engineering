# ✈️ Flight Operations Analytics – End-to-End Data Engineering Project

This project is a **real-world, end-to-end data engineering pipeline** built using **Apache Airflow** to ingest, process, and analyze **live flight operations data** from a public REST API.

It demonstrates how **Airflow is used in real production environments** — covering orchestration, scheduling, retries, idempotent pipelines, incremental processing, and analytics-ready data modeling using **Medallion Architecture (Bronze, Silver, Gold)**.

This project is designed as a **strong portfolio project** for **Data Engineering, Analytics Engineering, and Airflow-focused roles**.

---

## 📌 Project Overview

The pipeline ingests **live global flight activity data**, processes it through multiple transformation layers, and delivers **near-real-time analytics-ready datasets** suitable for BI dashboards such as **Power BI**.

The focus is on **pattern-level analytics**, not individual flight tracking.

---

## 🏗️ System Architecture

![Flight Operations Analytics Architecture](https://github.com/shreeramsundart/Real-Time-Flights-Analysis-Data-Engineering/blob/main/Flights%20Power%20BI%20Output.png)

### High-Level Flow
1. Pull live flight data from a public REST API
2. Orchestrate ingestion and transformations using Apache Airflow
3. Store raw API responses in the **Bronze layer**
4. Clean and normalize data in the **Silver layer**
5. Aggregate KPIs in the **Gold layer**
6. Load analytics-ready data into Snowflake
7. Enable near-real-time BI dashboards (Power BI ready)

---

## 🔄 Medallion Architecture

### 🥉 Bronze Layer – Raw Data
- Stores raw JSON responses from the live flight API
- Immutable, append-only ingestion
- Acts as a historical source of truth
- Enables reprocessing if logic changes

### 🥈 Silver Layer – Cleaned Data
- Normalizes and flattens flight records
- Handles missing values and schema consistency
- Applies basic validation and transformations
- Prepares data for analytical modeling

### 🥇 Gold Layer – Analytics Ready
- Aggregated flight KPIs and metrics
- Time-windowed (near-real-time batch processing)
- Incremental and historical storage
- Optimized for BI and reporting

---

## 🧠 Project Use Case

This project simulates how **aviation analytics and operations teams** analyze global flight activity to:

- Monitor air traffic volume trends
- Detect congestion or traffic spikes
- Compare flight activity across countries and regions
- Analyze time-based flight patterns
- Build historical datasets from live operational data

⚠️ **This is not air-traffic control software** — it focuses on **analytics and decision support**.

---

## 🚀 What You’ll Learn

By working through this project, you’ll learn how to:

- Pull live flight operations data from a real public API
- Build fully automated Airflow pipelines with scheduling
- Design and implement Medallion Architecture
- Process data in near-real-time (30-minute windows)
- Build rerunnable, idempotent data pipelines
- Handle retries, dependencies, and failures correctly
- Design incremental analytics tables
- Prepare data for BI dashboards
- Think like a production data engineer

---

## 🧰 Tech Stack

- **Apache Airflow** – Workflow orchestration
- **Python** – Data ingestion and processing
- **Snowflake** – Cloud data warehouse
- **REST API** – Live flight operations data
- **Docker & Docker Compose** – Containerized environment
- **Medallion Architecture** – Bronze → Silver → Gold
- **Power BI** – Analytics & visualization (optional)

---

## 📊 Project Highlights

- ✅ Real API ingestion (no CSVs, no mock data)
- ✅ Near-real-time batch analytics
- ✅ Production-style Airflow DAGs
- ✅ Clear separation of data layers
- ✅ Incremental and historical KPI storage
- ✅ Analytics-ready data modeling
- ✅ Clean, modular, portfolio-ready codebase

---

## 📈 Analytics Use Cases

The Gold layer enables dashboards such as:
- Flights per country per time window
- Global traffic trends over time
- Congestion detection signals
- Regional flight activity comparisons
- Historical air traffic analysis

---

## 🐳 Running the Project (High-Level)

```bash
docker-compose up -d


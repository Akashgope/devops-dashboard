# devops-dashboard
DevOps Dashboard - Multi-Cloud Cost Monitoring


Project Overview

"This project aims to build a centralized dashboard for monitoring resource usage and costs across AWS, Azure, and GCP. The dashboard will provide real-time and historical data visualization, cost threshold alerts, and drill-down capabilities by resource type and environment."

Section 2: Progress Report (What Has Been Completed)

✅ AWS Cost Explorer API integration with working aws_fetcher.py

✅ Azure Cost Management API integration with working azure_fetcher.py

✅ GCP Cloud Billing API connectivity with working gcp_fetcher.py

✅ Environment configuration with secure credential management

✅ Project folder structure and Python dependencies setup

Section 3: Proof of Work (Include Screenshots)

Screenshot 1: aws_fetcher.py running successfully (JSON output)

<img width="790" height="131" alt="Screenshot 2026-09-06 at 2 30 47 PM" src="https://github.com/user-attachments/assets/a5c778c9-6ac3-44a3-9004-36fdb52a4fc7" />


Screenshot 2: azure_fetcher.py running successfully (JSON output)

<img width="737" height="129" alt="Screenshot 2026-09-06 at 2 30 54 PM" src="https://github.com/user-attachments/assets/7e1a1705-5b02-483a-8289-ede1773715ad" />


Screenshot 3: gcp_fetcher.py running successfully (billing account list)

<img width="853" height="80" alt="Screenshot 2026-09-06 at 2 32 05 PM" src="https://github.com/user-attachments/assets/50709632-03cf-4f66-8b2e-c1e983d7e366" />


Screenshot 4: Project folder structure (tree or ls -la output)

<img width="859" height="383" alt="Screenshot 2026-09-06 at 2 46 52 PM" src="https://github.com/user-attachments/assets/c572866f-f693-44c8-a32f-faa861c73897" />


Screenshot 5: .env file (with credentials hidden/redacted)

<img width="862" height="246" alt="Screenshot 2026-09-06 at 2 47 42 PM" src="https://github.com/user-attachments/assets/a9f931c5-555a-463d-8800-a1e499604dca" />


Section 4: Sprint 2 Completion – Data Aggregation & Storage

### Overview
Sprint 2 focused on building the data aggregation and storage foundation. All cloud cost data is now standardized, stored in a PostgreSQL database, and automatically fetched daily.

### What Has Been Completed

✅ **PostgreSQL Database Setup** – Running in Docker container with persistent storage

✅ **Unified Database Schema** – Created `cost_usage` table with standardized fields for all cloud providers

✅ **Data Standardizer Module** – Converts AWS, Azure, and GCP data into a single unified format

✅ **Database Connector** – Bulk insert functionality with error handling and rollback support

✅ **Automated Data Pipeline** – All three fetchers now store data directly into PostgreSQL

✅ **Daily Scheduler** – Implemented using `schedule` library; runs daily at 10:00 AM

✅ **GCP BigQuery Integration** – Billing export enabled; cost data now queryable via BigQuery

### Data Pipeline Architecture
Cloud Providers → API Fetchers → Data Standardizer → PostgreSQL → Dashboard
AWS aws_fetcher.py Unified cost_usage (Sprint 3)
Azure azure_fetcher.py Schema Table
GCP gcp_fetcher.py

text

### Database Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `provider` | VARCHAR(20) | AWS, Azure, or GCP |
| `resource_id` | VARCHAR(255) | Unique resource identifier |
| `resource_type` | VARCHAR(100) | Compute, Storage, Database |
| `environment` | VARCHAR(50) | prod, dev, staging |
| `cost` | DECIMAL(15,6) | Daily cost in USD |
| `cpu_util_avg` | DECIMAL(5,2) | Average CPU utilization (%) |
| `memory_util_avg` | DECIMAL(5,2) | Average memory utilization (%) |
| `usage_date` | DATE | Date of cost/usage data |
| `raw_data` | JSONB | Original API response for debugging |
| `created_at` | TIMESTAMP | Record insertion timestamp |

### Screenshots from Sprint 2

**Screenshot 6: PostgreSQL Table Created**
[Insert screenshot of `psql` showing the `cost_usage` table structure]

<img width="2014" height="1180" alt="image" src="https://github.com/user-attachments/assets/0ae39d7e-62ad-4d54-8438-fa5117ff8765" />


**Screenshot 7: Data Successfully Inserted**
[Insert screenshot of `SELECT * FROM cost_usage LIMIT 5;` showing records]

<img width="1529" height="886" alt="image" src="https://github.com/user-attachments/assets/06e0df89-f8bf-4f31-b0c0-2045af12c613" />


**Screenshot 8: Scheduler Running Successfully**

<img width="1442" height="418" alt="image" src="https://github.com/user-attachments/assets/197df409-3d0f-4d62-be5a-37b508454b22" />


**Screenshot 9: GCP BigQuery Export Enabled**

<img width="3076" height="776" alt="image" src="https://github.com/user-attachments/assets/092cc60b-a1fe-45b4-8b01-f0f3debb2ed0" />


### Key Files Created in Sprint 2
src/data_processing/
├── init_db.py # Database initialization & table creation
├── standardizer.py # Unified data transformer (AWS, Azure, GCP)
└── db_connector.py # PostgreSQL insert logic

src/cloud_providers/
├── aws_fetcher.py # Updated with DB storage
├── azure_fetcher.py # Updated with DB storage
└── gcp_fetcher.py # Updated with BigQuery integration

src/
└── scheduler.py # Daily automated data pipeline



# 🚀 Sprint 3: Real-Time Dashboard Development – Completed ✅

## Overview

Sprint 3 successfully delivered the visualization layer for the DevOps Dashboard. A **FastAPI backend** now serves data from PostgreSQL through REST APIs, while a **React frontend** with Chart.js provides an interactive dashboard for real-time cost and resource monitoring.

The completed implementation connects the PostgreSQL database, FastAPI backend, and React frontend into a complete monitoring dashboard.

---

## ✅ What Has Been Completed

### 🔧 FastAPI Backend

The FastAPI backend provides three core REST API endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/api/current` | GET | Returns aggregated metrics including Total Cost, Average CPU, Average Memory, and Resource Count |
| `/api/historical` | GET | Returns daily cost trends for the last 30 days with provider-specific breakdowns |
| `/api/filters` | GET | Returns available filter options including Providers, Environments, and Resource Types |

The backend queries the PostgreSQL `cost_usage` table, applies the selected filters, performs the required aggregations, and returns the results as JSON responses.

---

## ⚛️ React Frontend

The frontend was built using **React** and provides an interactive dashboard for monitoring cloud resource usage and costs.

The dashboard includes:

- **4 Interactive Metric Cards**
  - Total Cost ($)
  - Average CPU (%)
  - Average Memory (%)
  - Total Resources

- **Cost Trend Line Chart**
  - Displays daily cost trends for the last 30 days
  - Provides provider-specific cost breakdowns
  - Supports AWS, Azure, and GCP

- **3 Dynamic Filters**
  - Provider: AWS / Azure / GCP
  - Environment: prod / dev / staging
  - Resource Type: Compute / Storage / Database

- **Data Refresh Button**
  - Allows users to manually refresh dashboard data from the backend API

---

## 🌐 Cross-Origin Resource Sharing (CORS)

CORS was configured in FastAPI to allow communication between the React frontend and FastAPI backend during development.

This allows the React application running on port `3000` to communicate with the FastAPI backend running on port `8000`.

---

🏗️ Architecture Flow

┌─────────────────────┐
│ PostgreSQL Database │
│                     │
│   cost_usage table  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   FastAPI Backend   │
│                     │
│    REST APIs        │
│    Port: 8000       │
└──────────┬──────────┘
           │
           │ HTTP / JSON
           ▼
┌─────────────────────┐
│   React Frontend    │
│                     │
│     Chart.js        │
│     Port: 3000      │
└──────────┬──────────┘
           │
           ▼
      User Browser



The PostgreSQL database stores cloud resource usage and cost information. The FastAPI backend retrieves and aggregates this information through REST APIs. The React frontend consumes the APIs using Axios and displays the results using interactive dashboard components and Chart.js visualizations.


📁 Key Files Added in Sprint 3

devops-dashboard/
│
├── src/
│   └── api/
│       └── main.py
│           └── FastAPI application with REST API endpoints
│
└── frontend/
    ├── src/
    │   ├── App.js
    │   │   └── Main application wrapper
    │   │
    │   ├── App.css
    │   │   └── Global application styles
    │   │
    │   └── components/
    │       └── Dashboard.js
    │           └── Dashboard metrics, charts, filters and API integration
    │
    ├── package.json
    │   └── React dependencies
    │
    └── README.md
        └── Frontend documentation


📊 API Endpoints Summary
| Endpoint                  | Method | Description                              | Example                                                                                                      |
| ------------------------- | ------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `/api/current`            | GET    | Returns aggregated current usage metrics | `{"total_cost": 125.50, "avg_cpu": 45.2, "avg_memory": 62.1, "resource_count": 25}`                          |
| `/api/historical?days=30` | GET    | Returns historical daily cost trends     | `{"labels": ["2026-09-01", "..."], "datasets": [...]}`                                                       |
| `/api/filters`            | GET    | Returns available filter options         | `{"providers": ["AWS", "Azure"], "environments": ["prod", "dev"], "resource_types": ["Compute", "Storage"]}` |



📸 Screenshots – Proof of Work
Screenshot 10: FastAPI Swagger UI Documentation

The FastAPI Swagger UI provides interactive API documentation and allows the REST endpoints to be tested directly from the browser.

<img width="1546" height="871" alt="Screenshot 2026-09-09 at 12 14 55 PM" src="https://github.com/user-attachments/assets/37f3f0e1-385b-499c-a64a-25f74fd1145a" />


Screenshot 11: FastAPI Current Usage API Response

The /api/current endpoint returns aggregated metrics such as total cost, average CPU usage, average memory usage, and total resources.

<img width="2730" alt="FastAPI Current Usage API Response" src="https://github.com/user-attachments/assets/3e310ca7-3a70-48e2-9d7e-845c36df6178">


Screenshot 12: FastAPI Historical Trends API Response

The /api/historical endpoint provides historical daily cost information and provider-specific breakdowns.

<img width="1330" alt="FastAPI Historical Trends API Response" src="https://github.com/user-attachments/assets/cca0a362-7f78-4f2a-88ee-b79a7a26e28e">


Screenshot 13: React Dashboard – Full View

The completed React dashboard displays real-time cost and resource metrics in an interactive user interface.

<img width="3024" alt="React Dashboard Full View" src="https://github.com/user-attachments/assets/3b913b52-d435-44e3-8972-c71ea2a76597">


Screenshot 14: React Dashboard – Filters in Action

The dashboard filters allow users to dynamically filter the displayed metrics based on cloud provider, environment, and resource type.

<img width="2720" alt="Dashboard Filters in Action" src="https://github.com/user-attachments/assets/3aba4178-46cb-41b7-b0f4-179ff06a8bc4">



🚀 HOW TO RUN THE COMPLETED SPRINT 3
====================================

------------------------------------------------------------
1. START POSTGRESQL
------------------------------------------------------------

If PostgreSQL is not already running, start the Docker container:

    docker start postgres-dashboard

Verify that the PostgreSQL container is running:

    docker ps


------------------------------------------------------------
2. START THE FASTAPI BACKEND
------------------------------------------------------------

Navigate to the project directory:

    cd devops-dashboard

Activate the Python virtual environment:

    source venv/bin/activate

Start the FastAPI application:

    python src/api/main.py

The backend will run on:

    http://localhost:8000


------------------------------------------------------------
3. START THE REACT FRONTEND
------------------------------------------------------------

Open a new terminal window and navigate to the frontend directory:

    cd devops-dashboard/frontend

Start the React application:

    npm start

The React dashboard will run on:

    http://localhost:3000


------------------------------------------------------------
4. ACCESS SWAGGER API DOCUMENTATION
------------------------------------------------------------

Open the following URL in your browser:

    http://localhost:8000/docs

This opens the interactive FastAPI Swagger UI where the available API endpoints can be tested.


✅ SPRINT 3 IS NOW COMPLETE AND RUNNING!



🧠 Challenges Faced & Solutions

| Challenge                                                     | Solution                                                                                  |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| CORS errors when React attempted to communicate with FastAPI  | Added `CORSMiddleware` to FastAPI with `allow_origins=["*"]` during development           |
| Chart.js rendering issues with large datasets                 | Limited historical data to 30 days and used `tension: 0.3` for smoother line curves       |
| React state management becoming complex with multiple filters | Used React `useState` and `useEffect` hooks; filter changes trigger automatic API refetch |
| Empty data when filters returned no matching records          | Added fallback UI messages and handled empty datasets gracefully                          |


💡 TECHNICAL HIGHLIGHTS
============================================================

METRIC CARDS
------------------------------------------------------------
The dashboard calculates the total cost using database-level 
aggregation:

    SUM(cost)

CPU and memory averages are calculated using:

    AVG(cpu)
    AVG(memory)

Performing these calculations at the database level reduces 
unnecessary processing in the frontend.


HISTORICAL COST CHART
------------------------------------------------------------
Historical cost data is grouped by:

    usage_date
    provider

This allows the dashboard to display separate cost trends for 
different cloud providers.

The chart supports:

    AWS
    Azure
    GCP

Historical data is limited to the previous 30 days to keep the 
visualization responsive and easy to understand.


FILTER INTEGRATION
------------------------------------------------------------
The dashboard sends filter selections to the FastAPI backend 
through query parameters.

For example:

    /api/current?provider=AWS&environment=prod

Multiple filters can also be combined:

    /api/current?provider=AWS&environment=prod&resource_type=Compute

This approach keeps the API flexible and makes filtered API 
requests easy to test and share.


============================================================
TECHNOLOGY STACK
============================================================

Technology        Purpose
------------------------------------------------------------
PostgreSQL        Database for cloud resource and cost information
FastAPI           Backend REST API
Python            Backend programming language
React             Frontend framework
Axios             HTTP/API communication
Chart.js          Data visualization
Docker            PostgreSQL containerization
Swagger UI        API documentation and testing


============================================================
SPRINT 3 OUTCOME
============================================================

Sprint 3 successfully delivered a complete visualization and 
API layer for the DevOps Dashboard.

The completed implementation provides:

    ✅ Real-time cost metrics
    ✅ CPU usage monitoring
    ✅ Memory usage monitoring
    ✅ Resource count monitoring
    ✅ Historical cost visualization
    ✅ AWS filtering
    ✅ Azure filtering
    ✅ GCP filtering
    ✅ Environment filtering
    ✅ Resource type filtering
    ✅ REST APIs
    ✅ Swagger API documentation
    ✅ Interactive React dashboard
    ✅ Chart.js visualizations
    ✅ Manual data refresh
    ✅ Graceful handling of empty datasets
    ✅ PostgreSQL integration
    ✅ FastAPI and React integration

The DevOps Dashboard now provides an end-to-end solution for 
monitoring cloud resource usage, infrastructure costs, and 
historical cost trends through an interactive web-based 
dashboard.

✅ SPRINT 3 COMPLETE

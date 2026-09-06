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
[Insert screenshot of `python src/scheduler.py` running with no errors]

**Screenshot 9: GCP BigQuery Export Enabled**
[Insert screenshot of GCP Console showing BigQuery billing export enabled]

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

text

### Technical Implementation Details

**1. PostgreSQL Setup**
```bash
docker run --name postgres-dashboard \
  -e POSTGRES_PASSWORD=your_secure_password \
  -e POSTGRES_DB=cloudcost \
  -p 5432:5432 \
  -d postgres:latest
2. Unified Data Standardization
Each provider's API response is transformed into a common format:

python
{
    'provider': 'AWS',
    'resource_id': 'i-12345',
    'resource_type': 'Compute',
    'environment': 'prod',
    'cost': 12.50,
    'cpu_util_avg': 45.2,
    'memory_util_avg': 60.1,
    'usage_date': '2026-09-06',
    'raw_data': '{...}'   # Original JSON for debugging
}
3. Automated Daily Scheduler

python
# Runs every day at 10:00 AM
schedule.every().day.at("10:00").do(run_all_fetchers)

# Fetches last 7 days of data from all providers
fetch_and_store_aws_costs(days_back=7)
fetch_and_store_azure_costs(days_back=7)
fetch_and_store_gcp_costs(days_back=7)
Verification Steps Completed
Test	Command	Result
PostgreSQL Running	docker ps | grep postgres	✅ Container Up
Table Created	\dt in psql	✅ cost_usage exists
AWS Data Inserted	SELECT COUNT(*) FROM cost_usage WHERE provider='AWS';	✅ Records found
Azure Data Inserted	SELECT COUNT(*) FROM cost_usage WHERE provider='Azure';	✅ Records found
GCP Data Inserted	SELECT COUNT(*) FROM cost_usage WHERE provider='GCP';	✅ Records found
Scheduler Test	python src/scheduler.py	✅ Runs without errors
text

---

## 🔄 Updated Next Steps Roadmap (After Sprint 2)

**Replace your existing Section 4 "Next Steps" with this updated version:**

```markdown
## Section 5: Next Steps (Roadmap)

| Sprint | Deliverable | Status |
|--------|-------------|--------|
| Sprint 1 | Cloud API Connectivity (AWS, Azure, GCP) | ✅ Completed |
| Sprint 2 | Data Aggregation & PostgreSQL Storage | ✅ Completed |
| Sprint 3 | Real-Time Dashboard (FastAPI + React/Grafana) | 🔄 In Progress |
| Sprint 4 | Historical Data Trends & Charts | 📋 Planned |
| Sprint 5 | Alerting & Slack/Teams Integration | 📋 Planned |
| Sprint 6 | Testing, Dockerization, Documentation | 📋 Planned |

### Sprint 3 Preview (Next Steps)
1. Build FastAPI backend with `/api/current` and `/api/historical` endpoints
2. Create React dashboard with Chart.js visualizations
3. Implement provider, resource type, and environment filters
4. Display cost trends and resource utilization metrics

Section 6: Conclusion

"The project has successfully established connectivity with all three major cloud providers (AWS, Azure, and GCP). Sprint 2 has now added a robust data aggregation and storage layer using PostgreSQL, with a unified schema that standardizes data from all providers. The daily scheduler ensures automated data collection, providing a solid foundation for the dashboard. The remaining sprints will focus on building the visualization layer (Sprint 3), implementing historical trend analysis (Sprint 4), setting up alerts (Sprint 5), and final deployment with Docker (Sprint 6). The project remains on track for full delivery within the planned timeline."


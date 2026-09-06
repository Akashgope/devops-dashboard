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


Section 4: Next Steps (Roadmap)

Sprint	Deliverable	Status
Sprint 2	Data Aggregation & PostgreSQL Storage	Planned
Sprint 3	Real-Time Dashboard (React/Grafana)	Planned
Sprint 4	Historical Data Trends & Charts	Planned
Sprint 5	Alerting & Slack/Teams Integration	Planned
Sprint 6	Testing, Docker, Documentation	Planned
Section 5: Challenges Faced & Solutions

"The GCP billing API does not provide a direct cost query endpoint like AWS and Azure. To fetch historical cost data, we will need to enable billing export to BigQuery and query the exported tables. This has been documented and will be addressed in Sprint 2."

Section 6: Conclusion

"The project has successfully established connectivity with all three major cloud providers (AWS, Azure, and GCP). The foundation for data aggregation is now complete. The remaining sprints will focus on storing this data, building the dashboard UI, implementing historical trends, and setting up alerts. With the current sprint completed on schedule, the project is on track for full delivery within the planned timeline."


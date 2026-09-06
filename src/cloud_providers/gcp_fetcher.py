import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
from google.cloud import bigquery
from datetime import datetime, timedelta
from src.data_processing.standardizer import standardize_gcp_data
from src.data_processing.db_connector import insert_cost_records

load_dotenv('config/.env')

def fetch_and_store_gcp_costs(days_back=7, environment='prod'):
    """
    Fetches GCP costs from the BigQuery billing export table.
    """
    try:
        client = bigquery.Client()

        table_id = os.getenv('GCP_BILLING_TABLE')
        
        if not table_id:
            print("⚠️ GCP: 'GCP_BILLING_TABLE' not set in .env. Skipping GCP data fetch.")
            return None

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        query = f"""
        SELECT 
            cost,
            usage_date,
            service.description as service_name,
            project.id as resource_id,
            location.location as region
        FROM `{table_id}`
        WHERE usage_date >= DATE('{start_date}')
        AND usage_date <= DATE('{end_date}')
        AND cost > 0
        ORDER BY usage_date DESC
        LIMIT 1000
        """

        print(f"🔍 Fetching GCP costs from {start_date} to {end_date}...")
        query_job = client.query(query)
        rows = query_job.result()

        records = standardize_gcp_data(rows, environment)

        if records:
            insert_cost_records(records)
            print(f"✅ Inserted {len(records)} GCP records.")
        else:
            print("⚠️ No GCP records found.")

        return rows

    except Exception as e:
        print(f"❌ Error fetching GCP costs: {str(e)}")
        return None

if __name__ == "__main__":
    fetch_and_store_gcp_costs()


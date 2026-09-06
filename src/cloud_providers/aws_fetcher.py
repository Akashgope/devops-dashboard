import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import boto3
from datetime import datetime, timedelta
from dotenv import load_dotenv
from src.data_processing.standardizer import standardize_aws_data
from src.data_processing.db_connector import insert_cost_records

load_dotenv('config/.env')

def fetch_and_store_aws_costs(days_back=7, environment='prod'):
    try:
        client = boto3.client(
            'ce',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        print(f"🔍 Fetching AWS costs from {start_date} to {end_date}...")

        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )

        records = standardize_aws_data(response, environment)
        
        if records:
            insert_cost_records(records)
        else:
            print("⚠️ No AWS records to insert.")

        return response

    except Exception as e:
        print(f"❌ Error fetching AWS costs: {str(e)}")
        return None

if __name__ == "__main__":
    fetch_and_store_aws_costs()


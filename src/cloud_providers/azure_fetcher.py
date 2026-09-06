import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod
from datetime import datetime, timedelta
from src.data_processing.standardizer import standardize_azure_data
from src.data_processing.db_connector import insert_cost_records

load_dotenv('config/.env')

def fetch_and_store_azure_costs(days_back=7, environment='prod'):
    try:
        tenant_id = os.getenv('AZURE_TENANT_ID')
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

        if not all([tenant_id, client_id, client_secret, subscription_id]):
            raise ValueError("Missing Azure credentials")

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        client = CostManagementClient(credential)
        scope = f"/subscriptions/{subscription_id}"

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        print(f"🔍 Fetching Azure costs from {start_date} to {end_date}...")

        query = QueryDefinition(
            type="ActualCost",
            timeframe="Custom",
            time_period=QueryTimePeriod(from_property=start_date, to=end_date),
            dataset={
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {
                        "name": "Cost",
                        "function": "Sum"
                    }
                },
                "grouping": []
            }
        )

        response = client.query.usage(scope=scope, parameters=query)

        records = standardize_azure_data(response, environment)
        
        if records:
            insert_cost_records(records)
        else:
            print("⚠️ No Azure records to insert.")

        return response

    except Exception as e:
        print(f"❌ Error fetching Azure costs: {str(e)}")
        return None

if __name__ == "__main__":
    fetch_and_store_azure_costs()


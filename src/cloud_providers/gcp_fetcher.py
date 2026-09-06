import os
from dotenv import load_dotenv
from google.cloud import billing_v1
from google.auth import credentials
import json
from datetime import datetime, timedelta

load_dotenv('config/.env')

def fetch_gcp_costs(days_back=7):
    try:
        # The path to the service account JSON is set in GOOGLE_APPLICATION_CREDENTIALS env var
        # Or we can explicitly pass it.
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path or not os.path.exists(creds_path):
            raise FileNotFoundError(f"GCP credentials file not found at {creds_path}")

        # Initialize the Cloud Billing Client
        client = billing_v1.CloudBillingClient()

        # Since we are using a service account key file, the client picks it up automatically.
        # To get cost data, we use the Cloud Catalog API to list SKUs,
        # BUT for actual billing data, we need the Cloud Billing Budget API or export to BigQuery.
        # For a simple test, we will list the billing accounts the service account has access to.

        print("🔍 Fetching GCP Billing Accounts...")
        request = billing_v1.ListBillingAccountsRequest()
        response = client.list_billing_accounts(request=request)

        print("✅ GCP Billing Accounts Retrieved:")
        for account in response.billing_accounts:
            print(f" - Name: {account.name}, Display Name: {account.display_name}, Open: {account.open}")

        # Note: To fetch actual cost data programmatically, you MUST export billing data to BigQuery.
        # GCP does not have a simple "Get Cost" API like AWS/Azure.
        # We will handle the BigQuery export in Sprint 2.
        # For now, we just confirm connectivity.

        return response

    except Exception as e:
        print(f"❌ Error fetching GCP data: {str(e)}")
        return None

if __name__ == "__main__":
    fetch_gcp_costs()


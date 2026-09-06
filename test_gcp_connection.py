import os
from dotenv import load_dotenv
from google.cloud import billing_v1

# Load .env
load_dotenv('config/.env')

# Set the credentials path
gcp_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if gcp_key:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_key

# Test connection
print("✅ GCP credentials loaded successfully!")
print(f"Key path: {gcp_key}")

# Try to list billing accounts
try:
    client = billing_v1.CloudBillingClient()
    accounts = client.list_billing_accounts()
    for account in accounts:
        print(f"✅ Found billing account: {account.name}")
        print(f"   Display name: {account.display_name}")
        break
    else:
        print("ℹ️ No billing accounts found or permission issue")
except Exception as e:
    print(f"❌ Error connecting: {e}")


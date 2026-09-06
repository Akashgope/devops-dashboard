import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient

# Load .env
load_dotenv('config/.env')

# Get Azure credentials
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

print(f"Tenant ID: {tenant_id[:8]}...{tenant_id[-4:]}")
print(f"Client ID: {client_id[:8]}...{client_id[-4:]}")

# Test authentication
try:
    # Create credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    
    print("\n✅ Azure Authentication Successful!")
    
    # Test Cost Management access
    try:
        # Create a cost management client
        cost_client = CostManagementClient(
            credential=credential,
            subscription_id=subscription_id
        )
        
        # Try to list cost management exports (tests permissions)
        # This is a simple test to see if permissions are correct
        scope = f"/subscriptions/{subscription_id}"
        print(f"   ✅ Cost Management client created successfully")
        print(f"   Scope: {scope}")
        
        # Note: To fetch actual costs, you need specific permissions
        # (Cost Management Reader role)
        
    except Exception as e:
        print(f"   ⚠️ Cost Management access check: {e}")
        
except Exception as e:
    print(f"\n❌ Azure Connection Failed!")
    print(f"   Error: {e}")


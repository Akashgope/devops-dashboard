import os
import boto3
from dotenv import load_dotenv

# Load .env
load_dotenv('config/.env')

# Get AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-east-1')

print(f"AWS Region: {aws_region}")
print(f"Access Key: {aws_access_key[:5]}...{aws_access_key[-4:]}")  # Mask for security

# Test credentials
try:
    # Create a client using the credentials
    client = boto3.client(
        'sts',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    
    # Get the caller identity (verifies credentials work)
    identity = client.get_caller_identity()
    print(f"\n✅ AWS Connection Successful!")
    print(f"   Account ID: {identity['Account']}")
    print(f"   User ARN: {identity['Arn']}")
    
    # Optional: Test Cost Explorer access
    # Note: This requires 'ce:GetCostAndUsage' permission
    try:
        ce_client = boto3.client(
            'ce',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        print("   ✅ Cost Explorer permissions: OK")
    except Exception as e:
        print(f"   ⚠️ Cost Explorer not accessible: {e}")
        
except Exception as e:
    print(f"\n❌ AWS Connection Failed!")
    print(f"   Error: {e}")


import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv('config/.env')

# Test GCP
gcp_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"GCP Key Path: {gcp_path}")

# Check if the file exists
if gcp_path and os.path.exists(gcp_path):
    print("✅ GCP key file found!")
else:
    print("❌ GCP key file NOT found")

# Test if the environment variable was set
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_path
print(f"GOOGLE_APPLICATION_CREDENTIALS is now: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")


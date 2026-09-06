
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schedule
import time
from src.cloud_providers.aws_fetcher import fetch_and_store_aws_costs
from src.cloud_providers.azure_fetcher import fetch_and_store_azure_costs
from src.cloud_providers.gcp_fetcher import fetch_and_store_gcp_costs

def run_all_fetchers():
    """Runs all cloud fetchers and stores data."""
    print("\n🔄 Running daily data aggregation...")
    
    fetch_and_store_aws_costs(days_back=7)
    fetch_and_store_azure_costs(days_back=7)
    fetch_and_store_gcp_costs(days_back=7)
    
    print("✅ Daily aggregation complete.\n")

# Schedule to run every day at 10:00 AM
schedule.every().day.at("10:00").do(run_all_fetchers)

print("🚀 Scheduler started. Waiting for 10:00 AM daily...")

# Run once immediately for testing
print("Running initial fetch now...")
run_all_fetchers()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute


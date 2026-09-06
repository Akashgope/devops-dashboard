import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('config/.env')

def get_connection():
    """Returns a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def create_tables():
    """Creates the unified cost_usage table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS cost_usage (
        id SERIAL PRIMARY KEY,
        provider VARCHAR(20) NOT NULL,          -- 'AWS', 'Azure', 'GCP'
        resource_id VARCHAR(255) NOT NULL,
        resource_type VARCHAR(100),             -- 'Compute', 'Storage', 'Database'
        environment VARCHAR(50),                -- 'prod', 'dev', 'staging'
        cost DECIMAL(15, 6) NOT NULL,
        cpu_util_avg DECIMAL(5, 2),             -- average CPU utilization (%)
        memory_util_avg DECIMAL(5, 2),          -- average Memory utilization (%)
        usage_date DATE NOT NULL,
        raw_data JSONB,                         -- store original API response for debugging
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes for fast queries
    CREATE INDEX IF NOT EXISTS idx_usage_date ON cost_usage(usage_date);
    CREATE INDEX IF NOT EXISTS idx_provider ON cost_usage(provider);
    """

    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database table 'cost_usage' is ready.")

if __name__ == "__main__":
    create_tables()


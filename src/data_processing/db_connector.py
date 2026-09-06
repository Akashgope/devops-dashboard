import os
import psycopg2
from psycopg2.extras import execute_values
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

def insert_cost_records(records):
    """
    Inserts multiple standardized records into the cost_usage table.
    """
    if not records:
        print("⚠️ No records to insert.")
        return False

    conn = get_connection()
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO cost_usage (
        provider, resource_id, resource_type, environment, 
        cost, cpu_util_avg, memory_util_avg, usage_date, raw_data
    ) VALUES %s
    """
    
    data_to_insert = [
        (
            rec['provider'],
            rec['resource_id'],
            rec['resource_type'],
            rec['environment'],
            rec['cost'],
            rec.get('cpu_util_avg'),
            rec.get('memory_util_avg'),
            rec['usage_date'],
            rec.get('raw_data', '{}')
        )
        for rec in records
    ]

    try:
        execute_values(cur, insert_query, data_to_insert)
        conn.commit()
        print(f"✅ Successfully inserted {len(records)} records into database.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting records: {e}")
        return False
    finally:
        cur.close()
        conn.close()


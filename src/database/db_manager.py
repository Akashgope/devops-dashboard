import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv('config/.env')

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'cloudcost'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'akash1990')
            )
            print("✅ Connected to PostgreSQL")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")

    def create_tables(self):
        """Create tables for storing cloud costs"""
        try:
            cursor = self.conn.cursor()

            # Create table for AWS costs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aws_costs (
                    id SERIAL PRIMARY KEY,
                    service VARCHAR(100),
                    cost DECIMAL(12, 4),
                    date DATE,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create table for Azure costs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS azure_costs (
                    id SERIAL PRIMARY KEY,
                    service VARCHAR(100),
                    cost DECIMAL(12, 4),
                    date DATE,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create table for GCP costs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gcp_costs (
                    id SERIAL PRIMARY KEY,
                    service VARCHAR(100),
                    cost DECIMAL(12, 4),
                    date DATE,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()
            print("✅ Tables created successfully")
            cursor.close()
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

    def insert_costs(self, table, data):
        """Insert cost data into a table"""
        try:
            cursor = self.conn.cursor()
            for service, cost in data.items():
                cursor.execute(f"""
                    INSERT INTO {table} (service, cost, date)
                    VALUES (%s, %s, CURDATE())
                """, (service, cost))
            self.conn.commit()
            print(f"✅ Inserted {len(data)} records into {table}")
            cursor.close()
        except Exception as e:
            print(f"❌ Error inserting data: {e}")

    def get_latest_costs(self, table, days=7):
        """Get cost data for the last N days"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f"""
                SELECT service, SUM(cost) AS total_cost
                FROM {table}
                WHERE date >= NOW() - INTERVAL '%s days'
                GROUP BY service
                ORDER BY total_cost DESC
            """, (days,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
    db.close()


import sqlite3
import csv
import os

def setup_database():
    csv_file = 'ad_data.csv'
    db_file = 'ads_data.db'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    print(f"Loading {csv_file} into SQLite...")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS ad_impressions")

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS ad_impressions (
        impression_id TEXT PRIMARY KEY,
        user_id TEXT,
        ad_id TEXT,
        timestamp TEXT,
        device_type TEXT,
        browser TEXT,
        geo TEXT,
        age_group TEXT,
        cpc_bid REAL,
        experiment_group TEXT,
        is_click INTEGER,
        is_registration INTEGER,
        is_conversion INTEGER
    );
    """
    cursor.execute(create_table_sql)
    
    # Read CSV and Insert
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) # Skip header
        
        # Batch insert
        rows = list(reader)
        
    insert_sql = "INSERT OR REPLACE INTO ad_impressions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.executemany(insert_sql, rows)
    conn.commit()
    
    # Verify
    cursor.execute("SELECT count(*) FROM ad_impressions")
    count = cursor.fetchone()[0]
    print(f"Successfully loaded {count} rows into 'ad_impressions' table.")
    
    conn.close()

if __name__ == "__main__":
    setup_database()

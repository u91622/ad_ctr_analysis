import sqlite3
import csv
import os

def setup_database():
    csv_file = 'ad_data.csv'
    db_file = 'ads_data.db'
    
    if not os.path.exists(csv_file):
        print(f"錯誤: 找不到 {csv_file}。")
        return

    print(f"正在將 {csv_file} 載入 SQLite...")
    
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
    
    # 讀取 CSV 並寫入
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) # 跳過標題列
        
        # 批次插入
        rows = list(reader)
        
    insert_sql = "INSERT OR REPLACE INTO ad_impressions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.executemany(insert_sql, rows)
    conn.commit()
    
    # 驗證
    cursor.execute("SELECT count(*) FROM ad_impressions")
    count = cursor.fetchone()[0]
    print(f"成功載入 {count} 筆資料至 'ad_impressions' 資料表。")
    
    conn.close()

if __name__ == "__main__":
    setup_database()

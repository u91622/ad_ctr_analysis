import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 設定優質的圖表風格
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

DB_FILE = 'ads_data.db'

def run_query(query, conn):
    return pd.read_sql_query(query, conn)

def main():
    if not os.path.exists(DB_FILE):
        print(f"找不到資料庫 {DB_FILE}。請先執行 setup_db.py。")
        return

    conn = sqlite3.connect(DB_FILE)
    print("已連線至資料庫...")

    # --- 1. 每日趨勢視覺化 ---
    print("正在分析每日趨勢...")
    query_daily = """
    SELECT 
        DATE(timestamp) as date,
        AVG(is_click) * 100 as ctr
    FROM ad_impressions
    GROUP BY 1 ORDER BY 1
    """
    df_daily = run_query(query_daily, conn)
    
    # Create reports directory if not exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_daily, x='date', y='ctr', marker='o', color='#4A90E2', linewidth=2.5)
    plt.title('Daily Click-Through Rate (CTR) Trend', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('CTR (%)')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/daily_ctr_trend.png')
    print("已儲存 reports/daily_ctr_trend.png")

    # --- 2. 裝置比較 ---
    print("正在分析裝置成效...")
    query_device = """
    SELECT 
        device_type,
        AVG(is_click) * 100 as ctr
    FROM ad_impressions
    GROUP BY 1
    """
    df_device = run_query(query_device, conn)
    
    plt.figure(figsize=(10, 6))
    pal = sns.color_palette("viridis", len(df_device))
    barplot = sns.barplot(data=df_device, x='device_type', y='ctr', palette=pal)
    plt.title('CTR by Device Type', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('CTR (%)')
    plt.xlabel('Device')
    
    # 加上數值標籤
    for i, v in enumerate(df_device['ctr']):
        barplot.text(i, v + 0.05, f"{v:.2f}%", ha='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('reports/device_ctr_comparison.png')
    print("已儲存 reports/device_ctr_comparison.png")

    # --- 3. A/B 測試結果 ---
    print("正在分析 A/B 測試結果...")
    query_ab = """
    SELECT 
        experiment_group,
        AVG(is_click) * 100 as ctr,
        SUM(is_conversion) * 1.0 / NULLIF(SUM(is_click), 0) * 100 as cvr
    FROM ad_impressions
    GROUP BY 1
    """
    df_ab = run_query(query_ab, conn)
    print("\n[A/B 測試發現]")
    print(df_ab)
    
    # 雙軸圖表
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Experiment Group')
    ax1.set_ylabel('CTR (%)', color=color)
    sns.barplot(data=df_ab, x='experiment_group', y='ctr', ax=ax1, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('CVR (%)', color=color)
    sns.lineplot(data=df_ab, x='experiment_group', y='cvr', ax=ax2, color=color, marker='s', markersize=10, linewidth=3)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('A/B Test: CTR vs CVR', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('reports/ab_test_result.png')
    print("已儲存 reports/ab_test_result.png")

    conn.close()
    print("\n分析完成。請查看生成的 PNG 圖檔。")

if __name__ == "__main__":
    main()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats # For statistical significance test

# Set style for professional visualization
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

DB_FILE = 'ads_data.db'

def run_query(query, conn):
    return pd.read_sql_query(query, conn)

def main():
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found. Please run setup_db.py first.")
        return

    conn = sqlite3.connect(DB_FILE)
    print("Connected to database...")
    
    # Create reports directory if not exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # --- 1. Daily Trend Visualization ---
    print("Analyzing daily trends...")
    query_daily = """
    SELECT 
        DATE(timestamp) as date,
        AVG(is_click) * 100 as ctr
    FROM ad_impressions
    GROUP BY 1 ORDER BY 1
    """
    df_daily = run_query(query_daily, conn)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_daily, x='date', y='ctr', marker='o', color='#4A90E2', linewidth=2.5)
    plt.title('Daily Click-Through Rate (CTR) Trend', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('CTR (%)')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/daily_ctr_trend.png')
    print("Saved reports/daily_ctr_trend.png")

    # --- 2. Device Comparison ---
    print("Analyzing device performance...")
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
    
    # Add data labels
    for i, v in enumerate(df_device['ctr']):
        barplot.text(i, v + 0.05, f"{v:.2f}%", ha='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('reports/device_ctr_comparison.png')
    print("Saved reports/device_ctr_comparison.png")

    # --- 3. A/B Test Results and Statistical Testing ---
    print("Analyzing A/B test results (including statistical testing)...")
    
    # (1) Extract raw data for t-test
    query_raw = "SELECT experiment_group, is_click FROM ad_impressions"
    df_raw = run_query(query_raw, conn)
    
    group_control = df_raw[df_raw['experiment_group'] == 'control']['is_click']
    group_test = df_raw[df_raw['experiment_group'] == 'test_creative_A']['is_click']
    
    t_stat, p_value = stats.ttest_ind(group_control, group_test)
    
    print(f"\n[A/B Statistical Test Results]")
    print(f"Control Group N={len(group_control)}, Test Group N={len(group_test)}")
    print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")
    if p_value < 0.05:
        print(">> Result: Significant - Reject Null Hypothesis")
    else:
        print(">> Result: Not Significant")
        
    # (2) Visualization
    query_ab = """
    SELECT 
        experiment_group,
        AVG(is_click) * 100 as ctr,
        SUM(is_conversion) * 1.0 / NULLIF(SUM(is_click), 0) * 100 as cvr
    FROM ad_impressions
    GROUP BY 1
    """
    df_ab = run_query(query_ab, conn)
    
    # Dual-axis chart
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
    
    plt.title(f'A/B Test Result (p={p_value:.3f})', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('reports/ab_test_result.png')
    print("Saved reports/ab_test_result.png")
    
    # --- 4. Funnel Analysis ---
    print("Running funnel analysis...")
    query_funnel = """
    WITH FunnelStats AS (
        SELECT 
            COUNT(*) as total_impressions,
            SUM(is_click) as total_clicks,
            SUM(is_registration) as total_registrations,
            SUM(is_conversion) as total_conversions
        FROM ad_impressions
    )
    SELECT '1.Impression' as step, total_impressions as count FROM FunnelStats
    UNION ALL
    SELECT '2.Click', total_clicks FROM FunnelStats
    UNION ALL
    SELECT '3.Registration', total_registrations FROM FunnelStats
    UNION ALL
    SELECT '4.Conversion', total_conversions FROM FunnelStats;
    """
    df_funnel = run_query(query_funnel, conn)
    print("\n[Funnel Data]")
    print(df_funnel)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_funnel, y='step', x='count', palette="magma")
    plt.title('Marketing Funnel: Imp -> Click -> Reg -> Conv', fontsize=16, fontweight='bold')
    plt.xlabel('Count')
    plt.ylabel('Funnel Step')
    plt.tight_layout()
    plt.savefig('reports/funnel_analysis.png')
    print("Saved reports/funnel_analysis.png")

    conn.close()
    print("\nAnalysis complete. Check generated PNG files.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

# 頁面配置
st.set_page_config(page_title="數位廣告分析儀表板", layout="wide")

DB_FILE = 'ads_data.db'

def load_data():
    if not os.path.exists(DB_FILE):
        return None
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM ad_impressions", conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    conn.close()
    return df

def main():
    st.title("數位廣告成效分析儀表板")
    st.markdown("本儀表板展示廣告點擊率 (CTR)、註冊率與轉換率的即時數據分析。")

    df = load_data()
    if df is None:
        st.error("找不到資料庫，請先執行 data_generator.py 和 setup_db.py。")
        return

    # 側邊欄過濾器
    st.sidebar.header("數據過濾")
    
    # 日期篩選
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    date_range = st.sidebar.date_input("選擇日期範圍", [min_date, max_date])
    
    # 裝置篩選
    devices = st.sidebar.multiselect("選擇裝置類型", options=df['device_type'].unique(), default=df['device_type'].unique())
    
    # 瀏覽器篩選
    browsers = st.sidebar.multiselect("選擇瀏覽器", options=df['browser'].unique(), default=df['browser'].unique())

    # 應用過濾
    mask = (df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1]) & \
           (df['device_type'].isin(devices)) & (df['browser'].isin(browsers))
    filtered_df = df[mask]

    # 關鍵指標 (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    
    total_imps = len(filtered_df)
    total_clicks = filtered_df['is_click'].sum()
    total_regs = filtered_df['is_registration'].sum()
    total_convs = filtered_df['is_conversion'].sum()
    
    ctr = (total_clicks / total_imps * 100) if total_imps > 0 else 0
    cvr = (total_convs / total_clicks * 100) if total_clicks > 0 else 0
    
    with col1:
        st.metric("總曝光數", f"{total_imps:,}")
    with col2:
        st.metric("總點擊數", f"{total_clicks:,}")
    with col3:
        st.metric("點擊率 (CTR)", f"{ctr:.2f}%")
    with col4:
        st.metric("轉換率 (CVR)", f"{cvr:.2f}%")

    st.divider()

    # 圖表區域
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("每日點擊率趨勢")
        daily_stats = filtered_df.groupby(filtered_df['timestamp'].dt.date)['is_click'].mean() * 100
        fig_trend = px.line(x=daily_stats.index, y=daily_stats.values, labels={'x': '日期', 'y': 'CTR (%)'})
        st.plotly_chart(fig_trend, use_container_width=True)

    with row1_col2:
        st.subheader("裝置類型佔比")
        device_counts = filtered_df['device_type'].value_counts()
        fig_pie = px.pie(values=device_counts.values, names=device_counts.index, hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("行銷漏斗分析")
        funnel_data = dict(
            number=[total_imps, total_clicks, total_regs, total_convs],
            stage=["曝光", "點擊", "註冊", "轉換"]
        )
        fig_funnel = px.funnel(funnel_data, x='number', y='stage')
        st.plotly_chart(fig_funnel, use_container_width=True)

    with row2_col2:
        st.subheader("A/B 測試成效")
        ab_stats = filtered_df.groupby('experiment_group')['is_click'].mean() * 100
        fig_ab = px.bar(x=ab_stats.index, y=ab_stats.values, labels={'x': '實驗組別', 'y': 'CTR (%)'}, color=ab_stats.index)
        st.plotly_chart(fig_ab, use_container_width=True)

if __name__ == "__main__":
    main()

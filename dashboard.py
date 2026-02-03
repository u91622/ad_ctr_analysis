import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(page_title="Ad Campaign Dashboard", layout="wide")

# Headers
st.title("Ad Campaign Dashboard")
st.markdown("### Real-time Analysis of CTR, CVR, and Funnel Metrics")

# Database Connection
DB_FILE = 'ads_data.db'

@st.cache_data
def load_data():
    if not os.path.exists(DB_FILE):
        st.error(f"Database {DB_FILE} not found. Please run setup_db.py first.")
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT * FROM ad_impressions"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Preprocessing
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    return df

df = load_data()

if df.empty:
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Date Filter
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Device Filter
device_options = ['All'] + list(df['device_type'].unique())
selected_device = st.sidebar.selectbox("Device Type", device_options)

# Filter Logic
mask = (df['date'] >= date_range[0]) & (df['date'] <= date_range[1])
if selected_device != 'All':
    mask = mask & (df['device_type'] == selected_device)

df_filtered = df[mask]

# --- KPI Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

total_imp = len(df_filtered)
total_clicks = df_filtered['is_click'].sum()
total_conv = df_filtered['is_conversion'].sum()
avg_cpc = df_filtered['cpc_bid'].mean()

ctr = (total_clicks / total_imp * 100) if total_imp > 0 else 0
cvr = (total_conv / total_clicks * 100) if total_clicks > 0 else 0

with col1:
    st.metric("Total Impressions", f"{total_imp:,.0f}")
with col2:
    st.metric("Click-Through Rate (CTR)", f"{ctr:.2f}%", delta_color="normal")
with col3:
    st.metric("Conversion Rate (CVR)", f"{cvr:.2f}%")
with col4:
    st.metric("Avg CPC", f"${avg_cpc:.2f}")

st.divider()

# --- Charts Section 1 ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Daily CTR Trend")
    daily_stats = df_filtered.groupby('date')['is_click'].mean().reset_index()
    daily_stats['ctr'] = daily_stats['is_click'] * 100
    
    fig_line = px.line(daily_stats, x='date', y='ctr', markers=True, 
                       labels={'ctr': 'CTR (%)'}, template="plotly_white")
    fig_line.update_traces(line_color='#4A90E2', line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("A/B Test Performance")
    ab_stats = df_filtered.groupby('experiment_group')[['is_click']].mean().reset_index()
    ab_stats['ctr'] = ab_stats['is_click'] * 100
    
    fig_bar = px.bar(ab_stats, x='experiment_group', y='ctr', color='experiment_group',
                     text_auto='.2f', labels={'ctr': 'CTR (%)'}, template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Charts Section 2 (Funnel) ---
st.subheader("Marketing Funnel Analysis")

funnel_data = {
    'Step': ['Impressions', 'Clicks', 'Registrations', 'Conversions'],
    'Value': [
        len(df_filtered),
        df_filtered['is_click'].sum(),
        df_filtered['is_registration'].sum(),
        df_filtered['is_conversion'].sum()
    ]
}
df_funnel = pd.DataFrame(funnel_data)

fig_funnel = go.Figure(go.Funnel(
    y = df_funnel['Step'],
    x = df_funnel['Value'],
    textposition = "inside",
    textinfo = "value+percent initial",
    marker = {"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
))
fig_funnel.update_layout(template="plotly_white")
st.plotly_chart(fig_funnel, use_container_width=True)

# --- Raw Data Preview ---
with st.expander("Show Raw Data Preview"):
    st.dataframe(df_filtered.head(100))

if __name__ == "__main__":
    pass # Streamlit processes the script directly

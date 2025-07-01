import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Uptime Monitor Dashboard", layout="wide")
st.title("🌐 Website Uptime Dashboard")

try:
    df = pd.read_csv("logs/history.csv", names=["timestamp", "url", "status", "response_time"])
except FileNotFoundError:
    st.error("No logs found yet.")
    st.stop()

df['timestamp'] = pd.to_datetime(df['timestamp'])

latest_status = df.sort_values('timestamp').groupby('url').tail(1)

def status_badge(status):
    return "✅" if status == "UP" else "❌"

st.markdown("### 🔍 Latest Website Statuses")
for _, row in latest_status.iterrows():
    col1, col2, col3 = st.columns([4, 1, 3])
    with col1:
        st.markdown(f"**{row['url']}**")
    with col2:
        st.markdown(status_badge(row['status']))
    with col3:
        st.markdown(f"*Last checked:* `{row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}`")

st.markdown("### 📈 Uptime Summary")
summary = df.groupby('url')['status'].value_counts().unstack().fillna(0)
summary['Uptime %'] = summary['UP'] / (summary['UP'] + summary['DOWN']) * 100
st.dataframe(summary[['Uptime %']].round(2))

if st.checkbox("📊 Show response time chart"):
    site = st.selectbox("Choose site", df['url'].unique())
    site_df = df[(df['url'] == site) & (df['response_time'] != "N/A")]
    site_df['response_time'] = site_df['response_time'].astype(float)
    st.line_chart(site_df.set_index("timestamp")["response_time"])
# dashboard.py
import streamlit as st
import pandas as pd
import os
import subprocess
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="UptimeGenie | Smart Monitor", layout="wide")

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.png", width=100)
with col_title:
    st.title("🦞‍♂️ UptimeGenie Dashboard")
    st.markdown("View the real-time status, uptime history, and response time trends for all monitored websites.")

st_autorefresh(interval=60_000, key="auto-refresh")

TELEGRAM_TOKEN = "7999119277:AAF-v2Xm2-Mmmu57uQ8KSy_BRGFtNSTOd5A"
CHAT_ID = "6002045226"

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        st.warning(f"Telegram Error: {e}")

# Ensure logs directory and file exists
if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("logs/history.csv"):
    with open("logs/history.csv", "w") as f:
        pass

# Add new website
st.subheader("➕ Add Website to Monitor")
with st.form("add_url_form"):
    new_url = st.text_input("Enter Website URL", placeholder="https://example.com")
    add_submit = st.form_submit_button("Add")
    if add_submit and new_url:
        try:
            response = requests.get(new_url, timeout=5)
            status = "UP" if response.status_code == 200 else "DOWN"
            response_time = int(response.elapsed.total_seconds() * 1000)
            now = datetime.utcnow().isoformat()
            with open("logs/history.csv", "a") as f:
                f.write(f"{now},{new_url},{status},{response_time}\n")
            st.success(f"✅ {new_url} is {status} — added successfully!")

            # Read all data and compile UP/DOWN lists
            df_all = pd.read_csv("logs/history.csv", header=None, names=["timestamp", "url", "status", "response_time"])
            df_all['timestamp'] = pd.to_datetime(df_all['timestamp'], errors='coerce')
            df_all.dropna(subset=['timestamp'], inplace=True)
            latest_all = df_all.sort_values('timestamp').drop_duplicates('url', keep='last')
            up_list = latest_all[latest_all['status'].str.upper() == 'UP']['url'].tolist()
            down_list = latest_all[latest_all['status'].str.upper() == 'DOWN']['url'].tolist()

            message = f"🦞‍♂️ New Website Added: {new_url}\nStatus: {status}\nResponse Time: {response_time} ms\n\n✅ UP Websites:\n" + \
                      "\n".join(up_list) + "\n\n❌ DOWN Websites:\n" + "\n".join(down_list)
            send_telegram_message(message)
        except Exception as e:
            st.error(f"❌ Could not reach site: {e}")

# Manual Global Check
if st.button("🌀 Run Immediate Check on All Sites"):
    subprocess.run(["python", "monitor.py"])
    st.experimental_rerun()

# Load all history
df_all = pd.read_csv("logs/history.csv", header=None, names=["timestamp", "url", "status", "response_time"])
df_all['timestamp'] = pd.to_datetime(df_all['timestamp'], errors='coerce')
df_all.dropna(subset=['timestamp'], inplace=True)
latest = df_all.sort_values('timestamp').drop_duplicates('url', keep='last')

# Website cards
st.subheader("📦 Website Status Blocks")
for _, row in latest.iterrows():
    box_color = "#e8f5e9" if row['status'].upper() == 'UP' else ("#ffebee" if row['status'].upper() == 'DOWN' else "#fff3e0")
    status_emoji = "🟢" if row['status'].upper() == 'UP' else ("🔴" if row['status'].upper() == 'DOWN' else "🟡")
    response = f"{row['response_time']} ms" if pd.notna(row['response_time']) else "N/A"

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div style='background-color:{box_color}; border: 1px solid #ccc; border-radius: 10px; padding: 1rem; margin-bottom: 2rem;'>
            <b>🌐 URL:</b> {row['url']}<br>
            <b>📊 Status:</b> {status_emoji} {row['status']}<br>
            <b>⚡ Response Time:</b> {response}<br>
            <b>🕒 Last Checked:</b> {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚀", key=f"manual_check_{row['url']}", help="Manual Recheck", use_container_width=True):
            try:
                response = requests.get(row['url'], timeout=5)
                status = "UP" if response.status_code == 200 else "DOWN"
                rt = int(response.elapsed.total_seconds() * 1000)
                now = datetime.utcnow().isoformat()
                with open("logs/history.csv", "a") as f:
                    f.write(f"{now},{row['url']},{status},{rt}\n")

                # Prepare updated UP/DOWN list
                df_all = pd.read_csv("logs/history.csv", header=None, names=["timestamp", "url", "status", "response_time"])
                df_all['timestamp'] = pd.to_datetime(df_all['timestamp'], errors='coerce')
                df_all.dropna(subset=['timestamp'], inplace=True)
                latest_all = df_all.sort_values('timestamp').drop_duplicates('url', keep='last')
                up_list = latest_all[latest_all['status'].str.upper() == 'UP']['url'].tolist()
                down_list = latest_all[latest_all['status'].str.upper() == 'DOWN']['url'].tolist()

                message = f"🔁 Manual Recheck for {row['url']}\nNew Status: {status}\nResponse Time: {rt} ms\n\n✅ UP Websites:\n" + \
                          "\n".join(up_list) + "\n\n❌ DOWN Websites:\n" + "\n".join(down_list)
                send_telegram_message(message)
                st.success(f"✅ {row['url']} rechecked successfully — Status: {status} ({rt} ms)", icon="✅")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Recheck failed: {e}")

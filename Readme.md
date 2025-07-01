# 🧞‍♂️ UptimeGenie – Smart Uptime Monitor

**UptimeGenie** is a lightweight, real-time, and modern uptime monitoring dashboard built using **Python**, **Streamlit**, and **Telegram Bot API**. Designed to act like your own uptime genie, it checks your websites, logs history, and alerts you instantly on failures — all without needing any third-party service.

---

## 📌 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🚀 Features](#-features)
- [📸 Dashboard Preview](#-dashboard-preview)
- [🔧 Tech Stack](#-tech-stack)
- [🛠️ Installation & Setup](#️-installation--setup)
- [🧪 Usage Guide](#-usage-guide)
- [📬 Telegram Integration](#-telegram-integration)
- [💡 How It Works](#-how-it-works)
- [🧠 Prompt Engineering Highlights](#-prompt-engineering-highlights)
- [📚 DevOps Relevance](#-devops-relevance)
- [🙌 Author](#-author)
- [📝 License](#-license)

---

## 🎯 Project Overview


UptimeGenie was built to demonstrate the power of **prompt engineering + DevOps automation** by solving a very real problem: keeping track of your websites’ health _without_ relying on costly external services.

This dashboard:

- Watches over any number of websites
- Checks status automatically or manually
- Alerts via Telegram
- Logs data with timestamps and response times
- Uses AI-crafted design and logic for a new-gen experience

---

## 🚀 Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🌐 Website Monitoring     | Add & track unlimited sites via dashboard                                   |
| 📊 Status Cards           | Color-coded blocks showing website status (UP/DOWN)                         |
| 🧠 Prompt-Based Design     | Entire dashboard UI and UX shaped by AI-guided prompt engineering            |
| 🚀 Manual Rechecks        | Instantly re-test any site with a click                                     |
| 📦 Local Logging          | Logs stored in CSV format for uptime history                                |
| 🕒 Auto Refresh           | Auto-refreshes every 60 seconds for live updates                            |
| 📬 Telegram Alerts        | Notifies you when a site goes DOWN or after manual recheck                  |
| 💡 Clean UI              | Streamlit-based responsive interface, optimized for desktop & tablet views  |

---


## 🔧 Tech Stack

- **Frontend / UI**: [Streamlit](https://uptime-genie---smart-uptime-monitor-cadet-07.streamlit.app/)
- **Backend Logic**: Python scripts
- **Live Updates**: `streamlit_autorefresh`
- **Notifications**: Telegram Bot API
- **Storage**: Local CSV logging
- **CI/CD (optional)**: GitHub Actions for scheduled monitoring

---

## 🛠️ Installation & Setup

### ✅ Prerequisites

- Python 3.8+
- pip

### 📦 Installation Steps

```bash
# 1. Clone the repo
git clone https://github.com/Jadav-Gajanand-19/Uptime-Genie---Smart-Uptime-Monitor.git
cd Uptime-Genie---Smart-Uptime-Monitor

# 2. Install dependencies
pip install -r requirements.txt

# 📊 Connectivity Downtime Tracker

A Streamlit web application that analyzes network/device connectivity logs to calculate downtime durations. The app takes a raw CSV export of device events, calculates the exact downtime from when a device goes **Down** until it comes back **Up**, and provides an interactive dashboard with summary statistics.

## ✨ Features
* **Drag-and-Drop Uploads**: Easily upload your `ConnectivityDownTime.csv` directly in the browser.
* **Summary Statistics**: Automatically calculates total outages, total downtime (in minutes), average downtime, and highlights the most affected device.
* **Device Breakdown**: View aggregated statistics grouped by device (e.g., Dishy1v4, TelOne).
* **Detailed Tracker**: A chronological, interactive table showing every downtime incident's Start, End, and Duration.
* **One-Click Export**: Download the cleaned and processed data as a new `Downtime_Tracker.csv` file.

## 📋 Prerequisites
Make sure you have [Python 3.8+](https://www.python.org/downloads/) installed on your computer.

## 🛠️ Installation

1. **Clone or Download the repository**
   Place `app.py`, `requirements.txt`, and this `README.md` in the same folder.

2. **Open your terminal or command prompt**
   Navigate to the folder where you saved the files.
   ```bash
   cd path/to/your/folder
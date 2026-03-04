import streamlit as st
import pandas as pd
import re
import io

# Set page configuration
st.set_page_config(page_title="Connectivity Downtime Tracker", page_icon="📊", layout="wide")

def process_downtime_data(df):
    """Processes the raw dataframe to calculate downtime durations."""
    
    # Extract device name and status securely
    def extract_device(event_str):
        match = re.search(r"'(.*?)'", str(event_str))
        return match.group(1) if match else "Unknown"

    df["Device"] = df["Event"].apply(extract_device)
    df["Status"] = df["Event"].apply(lambda x: "Up" if "Up" in str(x) else "Down")
    
    # Convert to datetime and drop invalid rows
    df["When"] = pd.to_datetime(df["When"], errors='coerce')
    df = df.dropna(subset=["When", "Device", "Status"])

    # Sort ascending (bottom-up order - chronological)
    df = df.sort_values(by="When", ascending=True).reset_index(drop=True)

    records = []
    
    # Group by device and calculate downtime
    for device, group in df.groupby("Device"):
        group = group.reset_index(drop=True)
        down_start = None

        for _, row in group.iterrows():
            if row["Status"] == "Down":
                down_start = row["When"]
            elif row["Status"] == "Up" and down_start is not None:
                duration = row["When"] - down_start
                records.append({
                    "Device": device,
                    "Downtime Start": down_start,
                    "Downtime End": row["When"],
                    "Duration (minutes)": round(duration.total_seconds() / 60, 2)
                })
                down_start = None

    return pd.DataFrame(records)

# --- APP UI ---
st.title("📊 Connectivity Downtime Tracker")
st.markdown("""
Upload your **ConnectivityDownTime.csv** file below. 
The app will automatically calculate downtime durations (from when a device goes **Down** until it comes back **Up**) and generate a clean tracker.
""")

# File Uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read file
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        if not all(col in df.columns for col in ["When", "Event"]):
            st.error("❌ Invalid file format. The CSV must contain 'When' and 'Event' columns.")
        else:
            with st.spinner("Processing data..."):
                downtime_df = process_downtime_data(df)
            
            if downtime_df.empty:
                st.warning("⚠️ No completed downtime records found in this file (e.g., no matching Down -> Up events).")
            else:
                st.success("✅ Data processed successfully!")
                
                # --- SUMMARY METRICS ---
                st.subheader("📈 Summary Statistics")
                summary_cols = st.columns(4)
                
                total_incidents = len(downtime_df)
                total_downtime = downtime_df["Duration (minutes)"].sum()
                avg_downtime = downtime_df["Duration (minutes)"].mean()
                most_affected = downtime_df.groupby("Device")["Duration (minutes)"].sum().idxmax()
                
                summary_cols[0].metric("Total Outages", total_incidents)
                summary_cols[1].metric("Total Downtime (mins)", round(total_downtime, 2))
                summary_cols[2].metric("Avg Downtime (mins)", round(avg_downtime, 2))
                summary_cols[3].metric("Highest Downtime Device", most_affected)

                # --- DEVICE BREAKDOWN ---
                st.subheader("🔍 Device Breakdown")
                device_summary = downtime_df.groupby("Device").agg(
                    Total_Outages=('Device', 'count'),
                    Total_Downtime_Mins=('Duration (minutes)', 'sum'),
                    Average_Downtime_Mins=('Duration (minutes)', 'mean')
                ).round(2).reset_index()
                st.dataframe(device_summary, use_container_width=True)

                # --- DETAILED TRACKER TABLE ---
                st.subheader("📝 Detailed Downtime Tracker")
                st.dataframe(downtime_df, use_container_width=True)
                
                # --- DOWNLOAD BUTTON ---
                csv_data = downtime_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Downtime Tracker CSV",
                    data=csv_data,
                    file_name="Downtime_Tracker.csv",
                    mime="text/csv",
                )

    except Exception as e:
        st.error(f"❌ An error occurred while reading the file: {e}")
else:
    st.info("👆 Please upload a CSV file to get started.")
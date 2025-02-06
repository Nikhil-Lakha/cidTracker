import streamlit as st
import pandas as pd
import os

# Define the CSV file to store data
DATA_FILE = "campaign_data.csv"

# Define column names
columns = [
    "Campaign Name", "Channel", "Campaign Type", "Campaign Objective",
    "Business Unit", "Business Product", "Start Date", "End Date",
    "Campaign Owner", "Target URL", "CID Campaign Link"
]

# Load existing data if file exists, otherwise create an empty DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

# Ensure correct data types for date columns
if not df.empty:
    df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df["End Date"] = pd.to_datetime(df["End Date"], errors="coerce")

# Display the editable data table
edited_df = st.data_editor(df, num_rows="dynamic")

# Save changes automatically when the table is updated
if not edited_df.empty:
    edited_df.to_csv(DATA_FILE, index=False)

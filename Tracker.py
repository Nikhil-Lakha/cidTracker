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

# Display the editable data table
edited_df = st.data_editor(df, num_rows="dynamic")

# Save changes automatically when the table is updated
if not edited_df.empty:
    edited_df.to_csv(DATA_FILE, index=False)

    # Identify the campaign with the latest start date
    most_recent_campaign = edited_df.loc[edited_df["Start Date"].idxmax()]["Campaign Name"]
    st.markdown(f"Your most recent campaign is **{most_recent_campaign}** 🚀")
